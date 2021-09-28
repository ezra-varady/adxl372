Python interface for adxl372 accelerometer. An alternative for the existing IIO driver because I find the interface confusing, and I imagine other people do too. Missing a few things documented below, but largely useable.

### Example
```
if __name__ == '__main__':
    from time import sleep
    from adxl372 import * 
    dev = ADXL372(0, 0)
    dev.set_op_mode(OP_MODES.STAND_BY)
    dev.set_autosleep(False)
    dev.set_bandwidth(BW.BW_3200Hz)
    dev.set_ODR(ODR.ODR_6400Hz)
    dev.set_op_mode(OP_MODES.FULL_BW_MEASUREMENT)
    print(dev.get_dev_id())
    print(dev.get_accel_data())
    print(ADXL372_SCALEG * dev.get_accel_data())
    datum = dev.get_accel_data()
    datum.x = datum.x * ADXL372_SCALEG
    datum.y = datum.y * ADXL372_SCALEG
    datum.z = datum.z * ADXL372_SCALEG
    print(datum)
 ```
 
 if you wish to scale the data the scale factor is calculated at the bottom of defs.py as ADXL372_SCALE
# TODO
- [x] FIFO support
- [ ] Trim Registers
- [ ] Interrupt Handling 


