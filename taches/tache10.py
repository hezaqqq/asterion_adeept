import time
import smbus
import tache3 as t3

class ADS7830(object):
    def __init__(self):
        self.cmd = 0x84
        self.bus=smbus.SMBus(1)
        self.address = 0x48 # 0x48 is the default i2c address for ADS7830 Module.   
        
    def analogRead(self, chn): # ADS7830 has 8 ADC input pins, chn:0,1,2,3,4,5,6,7
        value = self.bus.read_byte_data(self.address, self.cmd|(((chn<<2 | chn>>1)&0x07)<<4))
        return value

if __name__ == "__main__":
    adc = ADS7830()
        
    current_angle = 90 
    t3.set_angle(0, current_angle)
    
    STEP_SIZE = 5
    MIN_ANGLE = 0
    MAX_ANGLE = 180

    while True:
        adc_value = adc.analogRead(1)
        print(f"Light Tracking Value: {adc_value} | Current Angle: {current_angle}")
        
        if adc_value < 125:
            current_angle -= STEP_SIZE
            
        elif adc_value > 140:
            current_angle += STEP_SIZE
            
        else:
            pass

        if current_angle < MIN_ANGLE:
            current_angle = MIN_ANGLE
        elif current_angle > MAX_ANGLE:
            current_angle = MAX_ANGLE

        t3.set_angle(0, current_angle)

