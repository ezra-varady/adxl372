ADI_ADXL372_ADI_DEVID         = 0x00   # Analog Devices, Inc., accelerometer ID 
ADI_ADXL372_MST_DEVID         = 0x01   # Analog Devices MEMS device ID
ADI_ADXL372_DEVID             = 0x02   # Device ID
ADI_ADXL372_REVID             = 0x03   # product revision ID
ADI_ADXL372_STATUS_1          = 0x04   # Status register 1
ADI_ADXL372_STATUS_2          = 0x05   # Status register 2
ADI_ADXL372_FIFO_ENTRIES_2    = 0x06   # Valid data samples in the FIFO
ADI_ADXL372_FIFO_ENTRIES_1    = 0x07   # Valid data samples in the FIFO
ADI_ADXL372_X_DATA_H          = 0x08   # X-axis acceleration data [11:4]
ADI_ADXL372_X_DATA_L          = 0x09   # X-axis acceleration data [3:0] | dummy LSBs
ADI_ADXL372_Y_DATA_H          = 0x0A   # Y-axis acceleration data [11:4]
ADI_ADXL372_Y_DATA_L          = 0x0B   # Y-axis acceleration data [3:0] | dummy LSBs
ADI_ADXL372_Z_DATA_H          = 0x0C   # Z-axis acceleration data [11:4]
ADI_ADXL372_Z_DATA_L          = 0x0D   # Z-axis acceleration data [3:0] | dummy LSBs
ADI_ADXL372_X_MAXPEAK_H       = 0x15   # X-axis MaxPeak acceleration data [15:8]
ADI_ADXL372_X_MAXPEAK_L       = 0x16   # X-axis MaxPeak acceleration data [7:0]
ADI_ADXL372_Y_MAXPEAK_H       = 0x17   # X-axis MaxPeak acceleration data [15:8]
ADI_ADXL372_Y_MAXPEAK_L       = 0x18   # X-axis MaxPeak acceleration data [7:0]
ADI_ADXL372_Z_MAXPEAK_H       = 0x19   # X-axis MaxPeak acceleration data [15:8]
ADI_ADXL372_Z_MAXPEAK_L       = 0x1A   # X-axis MaxPeak acceleration data [7:0]
ADI_ADXL372_OFFSET_X          = 0x20   # X axis offset
ADI_ADXL372_OFFSET_Y          = 0x21   # Y axis offset
ADI_ADXL372_OFFSET_Z          = 0x22   # Z axis offset
ADI_ADXL372_X_THRESH_ACT_H    = 0x23   # X axis Activity Threshold [15:8]
ADI_ADXL372_X_THRESH_ACT_L    = 0x24   # X axis Activity Threshold [7:0]
ADI_ADXL372_Y_THRESH_ACT_H    = 0x25   # Y axis Activity Threshold [15:8]
ADI_ADXL372_Y_THRESH_ACT_L    = 0x26   # Y axis Activity Threshold [7:0]
ADI_ADXL372_Z_THRESH_ACT_H    = 0x27   # Z axis Activity Threshold [15:8]
ADI_ADXL372_Z_THRESH_ACT_L    = 0x28   # Z axis Activity Threshold [7:0]
ADI_ADXL372_TIME_ACT          = 0x29   # Activity Time
ADI_ADXL372_X_THRESH_INACT_H  = 0x2A   # X axis Inactivity Threshold [15:8]
ADI_ADXL372_X_THRESH_INACT_L  = 0x2B   # X axis Inactivity Threshold [7:0]
ADI_ADXL372_Y_THRESH_INACT_H  = 0x2C   # Y axis Inactivity Threshold [15:8]
ADI_ADXL372_Y_THRESH_INACT_L  = 0x2D   # Y axis Inactivity Threshold [7:0]
ADI_ADXL372_Z_THRESH_INACT_H  = 0x2E   # Z axis Inactivity Threshold [15:8]
ADI_ADXL372_Z_THRESH_INACT_L  = 0x2F   # Z axis Inactivity Threshold [7:0]
ADI_ADXL372_TIME_INACT_H      = 0x30   # Inactivity Time [15:8]
ADI_ADXL372_TIME_INACT_L      = 0x31   # Inactivity Time [7:0]
ADI_ADXL372_X_THRESH_ACT2_H   = 0x32   # X axis Activity2 Threshold [15:8]
ADI_ADXL372_X_THRESH_ACT2_L   = 0x33   # X axis Activity2 Threshold [7:0]
ADI_ADXL372_Y_THRESH_ACT2_H   = 0x34   # Y axis Activity2 Threshold [15:8]
ADI_ADXL372_Y_THRESH_ACT2_L   = 0x35   # Y axis Activity2 Threshold [7:0]
ADI_ADXL372_Z_THRESH_ACT2_H   = 0x36   # Z axis Activity2 Threshold [15:8]
ADI_ADXL372_Z_THRESH_ACT2_L   = 0x37   # Z axis Activity2 Threshold [7:0]
ADI_ADXL372_HPF               = 0x38   # High Pass Filter
ADI_ADXL372_FIFO_SAMPLES      = 0x39   # FIFO Samples
ADI_ADXL372_FIFO_CTL          = 0x3A   # FIFO Control
ADI_ADXL372_INT1_MAP          = 0x3B   # Interrupt 1 mapping control
ADI_ADXL372_INT2_MAP          = 0x3C   # Interrupt 2 mapping control
ADI_ADXL372_TIMING            = 0x3D   # Timing
ADI_ADXL372_MEASURE           = 0x3E   # Measure
ADI_ADXL372_POWER_CTL         = 0x3F   # Power control
ADI_ADXL372_SELF_TEST         = 0x40   # Self Test
ADI_ADXL372_SRESET            = 0x41   # Reset
ADI_ADXL372_FIFO_DATA         = 0x42   # FIFO Data

ADI_ADXL372_ADI_DEVID_VAL     = 0xAD   # Analog Devices, Inc., accelerometer ID
ADI_ADXL372_MST_DEVID_VAL     = 0x1D   # Analog Devices MEMS device ID
ADI_ADXL372_DEVID_VAL         = 0xFA   # Device ID
ADI_ADXL372_REVID_VAL         = 0x02   # product revision ID


MEASURE_AUTOSLEEP_MASK        = 0xBF
MEASURE_BANDWIDTH_MASK        = 0xF8
MEASURE_ACTPROC_MASK          = 0xCF
TIMING_ODR_MASK               = 0x1F
TIMING_WUR_MASK               = 0xE3
PWRCTRL_OPMODE_MASK           = 0xFC
PWRCTRL_INSTAON_THRESH_MASK   = 0xDF
PWRCTRL_INSTAON_THRESH_MASK   = 0xDF
PWRCTRL_FILTER_SETTLE_MASK    = 0xEF

# Position of flags in their respective registers
MEASURE_AUTOSLEEP_POS         = 6
MEASURE_ACTPROC_POS           = 4
TIMING_ODR_POS                = 5
TIMING_WUR_POS                = 2
INSTAON_THRESH_POS            = 5
FIFO_CRL_SAMP8_POS            = 0
FIFO_CRL_MODE_POS             = 1
FIFO_CRL_FORMAT_POS           = 3
PWRCTRL_FILTER_SETTLE_POS     = 4

DATA_RDY      = 1
FIFO_RDY      = 2
FIFO_FULL     = 4
FIFO_OVR      = 8

ADXL_SPI_RNW  = 1

#/*Acceleremoter configuration*/
ACT_VALUE       =  30     # Activity threshold value

INACT_VALUE     =  30     # Inactivity threshold value

ACT_TIMER       =  1      # Activity timer value in multiples of 3.3ms

INACT_TIMER     =  1      # Inactivity timer value in multiples of 26ms

ADXL_INT1_PIN   = 7
ADXL_INT2_PIN   = 5
ADXL_SPI_RNW    = 1

# + or - 200g with 12-bit resolution
# (200 + 200) * 9.81 / (2^12 - 1) = 0.958241 m/s^2 per lsb
ADXL372_SCALE = 0.958241
ADXL372_SCALEG = 0.09768 # g per lsb
