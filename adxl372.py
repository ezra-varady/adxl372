import spidev

from time import sleep
from enum import IntEnum
from dataclasses import dataclass

from defs import *


# Operating modes
class OP_MODES(IntEnum):
    STAND_BY = 0
    WAKE_UP = 1
    INSTANT_ON = 2
    FULL_BW_MEASUREMENT = 3

# Output Data Rates
class ODR(IntEnum):
    ODR_400Hz = 0
    ODR_800Hz = 1
    ODR_1600Hz = 2
    ODR_3200Hz = 3
    ODR_6400Hz = 4

# Filter Bandwidth (should be no more than half ODR)
class BW(IntEnum):
    BW_200Hz = 0
    BW_400Hz = 1
    BW_800Hz = 2
    BW_1600Hz = 3
    BW_3200Hz = 4

# Wake up rates
class WUR(IntEnum):
    WUR_52ms = 0
    WUR_104ms = 1
    WUR_208ms = 2
    WUR_512ms = 3
    WUR_2048ms = 4
    WUR_4096ms = 5
    WUR_8192ms = 6
    WUR_24576ms = 7

# Activity detection modes
class ActivityMode(IntEnum):
    DEFAULT = 0
    LINKED = 1
    LOOPED = 2

# Data format of FIFO queeu
class FIFOFormat(IntEnum):
    XYZ_FIFO = 0
    X_FIFO = 1
    Y_FIFO = 2 
    XY_FIFO = 3
    Z_FIFO = 4 
    XZ_FIFO = 5
    YZ_FIFO = 6
    XYZ_PEAK_FIFO = 7

# FIFO operating modes
class FIFOMode(IntEnum):
    BYPASSED = 0
    STREAMED = 1
    TRIGGERED = 2
    OLDEST_SAVED = 3

# Instant on impact detection threshold
class InstantOnThresh(IntEnum):
    ADXL_INSTAON_LOW_THRESH = 0 # 10-15g
    ADXL_INSTAON_HIGH_THRESH = 1 # 30-40g

# Filter settle time on wakeup
class FilterSettle(IntEnum):
    FILTER_SETTLE_370 = 0
    FILTER_SETTLE_16 = 1 # best for when filters are disabled

@dataclass
class Sample:
    x: int
    y: int
    z: int

class ADXL372:
    def __init__(self, major, minor):
        self.dev = spidev.SpiDev(major, minor)
        self.dev.max_speed_hz = 10**7
        self.dev.open(major, minor)

        # Registers start out zeroed except when otherwise stated
        self.op_mode = OP_MODES.FULL_BW_MEASUREMENT
        self.odr = ODR.ODR_400Hz
        self.bw = BW.BW_200Hz
        self.autosleep = False
        self.wakeup_rate = WUR.WUR_52ms
        self.activity_mode = ActivityMode.DEFAULT
        self.filter_settle = FilterSettle.FILTER_SETTLE_370
        self.instant_on_thresh = InstantOnThresh.ADXL_INSTAON_LOW_THRESH
        self.act_time_ms = 6.6
        self.inact_time_ms = 26
        self.fifo_samples = 0x80 # This is the default register value
        self.fifo_mode = FIFOMode.XYZ_FIFO
        self.fifo_format = FIFOFormat.BYPASSED

    def read(self, reg, nbytes=1):
        reg = reg << 1 | ADXL_SPI_RNW
        data = self.dev.xfer([reg] + [0x00] * nbytes)
        if len(data) == 2:
            return data[1]
        else:
            return data[1:]

    def write(self, reg, msg):
        reg = reg << 1
        if type(msg) != list:
            if type(msg) == int:
                msg = [msg]
            else:
                raise TypeError('msg must be int or list')

        self.dev.xfer([reg] + msg)

    def update(self, reg, mask, shift, val):
        old = self.read(reg)
        new = old & mask
        # xor oxff cause python's bitwise not is signed 
        new |= (val << shift) & (mask ^ 0xff)
        self.write(reg, new)

    def set_op_mode(self, mode: OP_MODES):
        '''
        Set the devices operating mode. STANDBY places the device in a 
        low-current mode wherein measurements are not taken. INSTANT_ON 
        places the device in low-current mode, and when activity within
        the INSTANT_ON_THRESHOLD is detected enters MEASUREMENT mode.
        In WAKEUP mode the device sleeps for the duration of the wake up 
        rate then wakes for the duration of the filter settle time. If 
        motion is detected an interrupt can be sent or the device can be
        switched into MEASUREMENT mode.

        mode: One of the operating modes defined in the OP_MODES enum
        '''
        self.update(ADI_ADXL372_POWER_CTL,
                PWRCTRL_OPMODE_MASK,
                0,
                mode)
        self.op_mode = mode

    def set_ODR(self, odr: ODR):
        '''
        Set the output data rate. This is essentially the sampling rate
        odr: One of the predefined data rates in the ODR enum
        '''
        self.update(ADI_ADXL372_TIMING,
                TIMING_ODR_MASK,
                TIMING_ODR_POS,
                odr)
        self.odr = odr

    def set_bandwidth(self, bandwidth: BW):
        '''
        Set the bandwidth of the internal 4-pole filters. This should be
        no more than half ofthe ODR

        bandwidth: One of the predefined bandwidths in the BW enum
        '''
        self.update(ADI_ADXL372_MEASURE,
                MEASURE_BANDWIDTH_MASK,
                0,
                bandwidth)
        self.bw = bandwidth

    def set_autosleep(self, enable: bool):
        '''
        If autosleep is set, when the device is in wake-up mode it will
        enter measurement mode upon detection of activity and reenter 
        wake-up mode on detection of inactivity.

        enable: Set to enable autosleep, unset to disable
        '''
        self.update(ADI_ADXL372_MEASURE,
                MEASURE_AUTOSLEEP_MASK,
                MEASURE_AUTOSLEEP_POS,
                int(enable))
        self.autosleep = enable

    def set_wakeup_rate(self, rate: WUR):
        '''
        Set the wake-up rate. Set the duration of the power down phase of 
        wake-up mode behavior to one of the preset values

        rate: One of the predefined wake-up rates in the WUR enum
        '''
        self.update(ADI_ADXL372_TIMING,
                TIMING_WUR_MASK,
                TIMING_WUR_POS,
                rate)
        self.wakeup_rate = rate

    def set_activity_processing_mode(self, mode: ActivityMode):
        '''
        Set the processing mode for activity/inactivity detection. In DEFAULT mode 
        they operate simultaneously, the user is responsible for reading and clearing
        the interrupts. In LINKED mode, it looks for only inactivity or activity.
        When activity is detected it looks for inactivity and vice versa the user
        must service interrupts. In LOOPED mode, the device behaves as in linked mode, 
        but the user doesn't have to service interrupts.

        mode: One of the activity modes defined in the ActivityMode enum
        '''
        self.update(ADI_ADXL372_MEASURE,
                MEASURE_ACTPROC_MASK,
                MEASURE_ACTPROC_POS,
                mode)
        self.activity_mode = mode

    def set_filter_settle(self, mode: FilterSettle):
        '''
        Set the filter settling time. leave this at 370ms if using either of the 
        internal filters. If neither is in use, it can be set to 16ms

        mode: The filter settling time defined in the FilterSettle enum
        '''
        self.update(
            ADI_ADXL372_POWER_CTL, PWRCTRL_FILTER_SETTLE_MASK, PWRCTRL_FILTER_SETTLE_POS, mode
        )
        self.filter_settle = mode

    def set_instant_on_thresh(self, mode: InstantOnThresh):
        '''
        Configure the threshold for instant-on activity detection.
        The default is 10-15g, but it can be configured to 30-40g.

        mode: One of the two instant-on thresholds defined in the InstantOnThresh enum
        '''
        self.update(ADI_ADXL372_POWER_CTL,
                PWRCTRL_INSTAON_THRESH_MASK,
                INSTAON_THRESH_POS,
                mode)
        self.instant_on_thresh = mode

    def get_dev_id(self):
        '''
        Returns the content of the device id. If it's not 0xAD somethign is wrong
        '''
        return self.read(ADI_ADXL372_ADI_DEVID)

    def get_status(self):
        '''
        Read the STATUS1 register to get information about device state
        for a breakdown of the fields check page 33 of the datasheet
        '''
        return self.read(ADI_ADXL372_STATUS_1)

    def get_activity_status(self):
        '''
        Read the STATUS2 register to get information about activity detection state
        for a breakdown of the fields check page 33 of the datasheet
        '''
        return self.read(ADI_ADXL372_STATUS_2)

    def set_activity_threshold(
            self,
            thresh: int,
            referenced: bool,
            enabled: bool,
            addr: int,
            multiple: bool=True):
        '''
        Set the activity thresholds. The default behavior is to set all three pairs and assumes 
        you're starting in one of the x axis msb registers, ADI_ADXL372_X_THRESH_ACT_H, 
        ADI_ADXL372_X_THRESH_ACT2_H, ADI_ADXL372_X_THRESH_INACT_H. If you wish to set a single
        register you can do this by setting multiple to false. The ACT2 registers control the
        motion warning subsystem which can issue an interrupt or set the status bit. It does not
        interact with linked or looped activity detection

        Thresh: The threshold in units of mg. It will be converted to the corresponding 11-bit code
        the scale factor is 100 mg/code.
        referenced: set reference for referenced activity processing. unset for absolute.
        enabled: set enabled to use the acis for activity detection. unset to ignore
        addr: Address of the threshold register you would like to set. Probably one of the three 
        listed above
        multiple: Defaults to true, if you want to set only a single pair of registers unset it
        '''

        #op_mode = self.read(ADI_ADXL372_POWER_CTL) & (PWRCTRL_OPMODE_MASK ^ 0xff)
        #self.set_op_mode(OP_MODES.STAND_BY)
        # TODO: break these registers out
        scaled = thresh // 100 # force integer division
        thresh = scaled & 0x7FF # make sure its 11 bits
        x_msb = [
            ADI_ADXL372_X_THRESH_ACT_H, 
            ADI_ADXL372_X_THRESH_ACT2_H, 
            ADI_ADXL372_X_THRESH_INACT_H
        ]

        referenced = int(referenced)
        enabled = int(enabled)

        thresh_high = thresh >> 3
        thresh_low = ((thresh << 5) | (referenced << 1) | enabled) & 0xFF

        w_data = [thresh_high, thresh_low]
        if multiple:
            # The Referenced bit only matters for X axes but it should be fine to replicate
            w_data = w_data * 3
            if not addr in x_msb:
                raise Exception(
                    'address was not set to one of the x msb registers, but multiple is set. This is likely an error'
                )

        self.write(addr, w_data)

    # TODO: break the code in set activity and inactivity out into a separate helper
    def set_activity_time(self, duration_ms: int):
        '''
        Set the activity detection time in milliseconds
        Activity detection is driven by an internal timer. Activity whose duration
        does not exceed a given number of periods of this timer will be ignored. If
        the ODR is 6.4kHz the period of this timer is 3.3ms, at all other ODRs it 
        is 6.6ms. This function will convert a time in ms to a number of periods 
        and set the correct register. Setting it to 0 will give 1 period detection
        the longest acceptable period is ~1.68s

        duration_ms: the duration in ms of events you wish to detect in ms
        '''
        # the driver multiplies everything here by 1000, possibly for less error
        # TODO: validate that not doing this is ok
        if self.odr == ODR.ODR_6400Hz:
            scale = 3.3
        else:
            scale = 6.6

        w_val = duration_ms / scale
        w_val = int(w_val + .5) # Bootleg positive integer rounding

        if w_val > 0xFF:
            w_val = 0xFF
        self.write(ADI_ADXL372_TIME_ACT, w_val)
        self.act_time_ms = duration_ms

    def set_inactivity_time(self, duration_ms: int):
        '''
        Similar to the activity timer. Set the number of periods to qualify 
        inactivity. The period for a 6.4kHz ODR is 13ms, for 3.2kHz and below
        it is 26ms. The maximum inactivity time is 28.4 minutes at 3.2kHz and
        below and 14.2 minutes at 6.4kHz

        duration_ms: the duration in ms of the inactivity events you wish to detect
        '''
        if self.odr == ODR.ODR_6400Hz:
            scale = 13
        else:
            scale = 26

        w_val = duration_ms / scale
        w_val = int(w_val + .5) # Bootleg positive integer rounding

        # this condition is probably redundant
        if w_val > 0xFFFF:
            w_val = 0xFFFF

        w_val_high = (w_val >> 8) & 0xFF
        w_val_low = w_val & 0xFF

        self.write(ADI_ADXL372_TIME_INACT_H, w_val_high)
        self.write(ADI_ADXL372_TIME_INACT_L, w_val_low)
        self.inact_time_ms = duration_ms

    @staticmethod
    def process_sample(data) -> Sample:
        '''
        Function to process samples, handles all the gross conversions
        needed to handle the accelerometers data format
        '''
        x = ((data[0] & 0xFF) << 8) | data[1]
        y = ((data[2] & 0xFF) << 8) | data[3]
        z = ((data[4] & 0xFF) << 8) | data[5]

        x = x >> 4
        y = y >> 4
        z = z >> 4

        def twos_complement(val):
            if (val & (1 << (12 - 1))):
                val = val - (1 << 12)
            return val


        x = twos_complement(x)
        y = twos_complement(y)
        z = twos_complement(z)

        return Sample(x, y, z)

    def get_highest_peak_accel_data(self) -> Sample:
        '''
        The FIFO can be configured so that it only records the peak
        impact events. While configured this way, the overall max 
        is stored in the MAXPEAK_X_X registers read here
        '''
        data = self.read(ADI_ADXL372_X_MAXPEAK_H, 6)
        return self.process_sample(data)

    def get_accel_data(self) -> Sample:
        '''
        Read the raw acceleration data for all three axes from the
        X_DATA_X register
        '''
        status = 0
        while not (status & DATA_RDY):
            status = self.get_status()

        data = self.read(ADI_ADXL372_X_DATA_H, 6)
        return self.process_sample(data)

    def get_fifo_entries(self) -> int:
        '''
        Returns the number of samples currently available in the FIFO.
        The 2 MSB are stored in FIFO_ENTRIES_2, the 8 LSB in FIFO_ENTRIES_1
        '''
        data = self.read(ADI_ADXL372_FIFO_ENTRIES_2, 2)
        data[0] = data[0] & 0x3
        ret_val = (data[0] << 8) | data[1]
        return ret_val

    def configure_fifo(self,
            samples: int,
            mode: FIFOMode,
            qformat: FIFOFormat): #TODO: think of a better name
        '''
        Configure the internal FIFO queue. This function simultaneously sets the 
        number of samples up to 512, the format of the samples (x-y-z, z, x-z, etc),
        and the mode the FIFO operates in. Note that for 3-axis and impact peak 
        the samples can be set to a max of 170, and for 2-axis a max of 256. The 
        512 sample maximum is only for single axis measurements. There are several
        modes, in BYPASS the FIFO is disabled, in OLDEST_SAVED the FIFO will store 
        the first N samples, and must be disabled and reenabled to collect a new set,
        in STREAMED mode it essentially acts like a buffer, holding the last N, and
        in TRIGGERED it acts like stream mode till an event, after which it stores 
        the samples around the event

        samples: The number of samples stored, should be informed by the format arg
        mode: The mode the FIFO will operate in, 
        qformat: The format that samples should be stored in, chooses axes to be sampled
        '''
        # FIFO must be configured in standby
        self.set_op_mode(OP_MODES.STAND_BY)

        if samples > 512 or samples < 0:
            samples = 512
        # You have to leave 1 sample in the FIFO queue when you read
        samples -= 1

        samples_msb = int(samples > 0xFF)
        config = (mode << FIFO_CRL_MODE_POS) | (qformat << FIFO_CRL_FORMAT_POS) | (samples_MSB << FIFO_CRL_SAMP8_POS)

        self.write(ADI_ADXL372_FIFO_SAMPLES, samples & 0xFF)
        self.write(ADI_ADXL372_FIFO_CTL, config)

        self.fifo_samples = samples + 1
        self.fifo_mode = mode
        self.fifo_format = qformat

        self.set_op_mode(OP_MODES.FULL_BW_MEASUREMENT)

    def reset(self):
        self.write(ADI_ADXL372_SRESET, 0x52)
        sleep(1)




if __name__ == '__main__':
    from time import sleep
    dev = ADXL372(0, 0)
    dev.set_op_mode(OP_MODES.STAND_BY)
    dev.set_autosleep(False)
    dev.set_bandwidth(BW.BW_3200Hz)
    dev.set_ODR(ODR.ODR_6400Hz)
    dev.set_op_mode(OP_MODES.FULL_BW_MEASUREMENT)
    print(dev.get_dev_id())
    print(dev.get_accel_data())
    sleep(1)
    print(dev.get_accel_data())
    sleep(1)
    print(dev.get_accel_data())
    sleep(1)
    print(dev.get_accel_data())
