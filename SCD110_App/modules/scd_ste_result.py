import struct
from typing import ValuesView

# helper for signed 16bit conversion
def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def s16floatfactor(value,factor):
    temp = s16(value[0] | (value[1]<<8))
    temp = float(temp)*factor
    return temp

def s16floatdiv(value,div):
    temp = s16(value[0] | (value[1]<<8))
    temp = float(temp)/div
    return temp

def s32floatfactor(value,factor):
    temp = value[0] | (value[1]<<8) | (value[2]<<16) | (value[3]<<24)
    temp = float(temp)*factor
    return temp

def int_(name,bytes,unit,factor=1,order="little",signed=True):
    cal = int.from_bytes(bytes, byteorder=order, signed=signed) 
    print("Value : {0} {1} : {2}".format(cal * factor,unit,name))

def short_(name,byte,factor=1,signed=True):
    cal = int(byte) 
    print("Value : {0} : {1}".format(cal,name))

def substrpad(str11,no,char):
    str11 = str11.ljust(no,char)
    return str11[0:no]

value = b'\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\xae\r\x90\xb9\x01\x00\xbe\x01\xa6\x00"\x01\x00\x00\x8f'

def printCharacteristic(bytes):
    value = bytes
    print(len(value))

    global Values
    global ValuesAsText
    ValuesAsText = []
    Values = []
    #0-1 accelArithmMean_x int16_t mg/LSB - convert factor = * 100
    temp = s16floatfactor(value[0:2],100.0)
    Values.append(temp)
    ValuesAsText.append("accelArithmMean_x -Value : {0} mg : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} mg : accelArithmMean_x".format(substrpad(str(temp),10," ")))
    #2-3 accelArithmMean_y int16_t mg/LSB - convert factor = * 100
    temp = s16floatfactor(value[2:4],100.0)
    Values.append(temp)
    ValuesAsText.append("accelArithmMean_y -Value : {0} mg : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} mg : accelArithmMean_y".format(substrpad(str(temp),10," ")))
    #4-5 accelArithmMean_z int16_t mg/LSB - convert factor = * 100
    temp = s16floatfactor(value[4:6],100.0)
    Values.append(temp)
    ValuesAsText.append("accelArithmMean_z -Value : {0} mg : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} mg : accelArithmMean_z".format(substrpad(str(temp),10," ")))
    #6-9 accelVariance_x uint32_t 10-²g²/LSB - convert factor = * 10
    temp = s32floatfactor(value[6:10],0.01)
    Values.append(temp)
    ValuesAsText.append("accelVariance_x   -Value : {0} g² : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} g² : accelVariance_x".format(substrpad(str(temp),10," ")))
    #10-13 accelVariance_y uint32_t 10-²g²/LSB - convert factor = * 10
    temp = s32floatfactor(value[10:14],0.01)
    Values.append(temp)
    ValuesAsText.append("accelVariance_y   -Value : {0} g² : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} g² : accelVariance_y".format(substrpad(str(temp),10," ")))
    #14-17 accelVariance_z uint32_t 10-²g²/LSB - convert factor = * 10
    temp = s32floatfactor(value[14:18],0.01)
    Values.append(temp)
    ValuesAsText.append("accelVariance_z   -Value : {0} g² : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} g² : accelVariance_z".format(substrpad(str(temp),10," ")))
    #18-19 temperatureRawValue int16_t °C/LSB - convert factor = * 0.0078
    temp = s16floatfactor(value[18:20],0.0078)
    Values.append(temp)
    ValuesAsText.append("temperature       -Value : {0} °C : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} °C : temperature".format(substrpad(str(temp),10," ")))
    #20-23 lightRawValue uint32_t mililux - convert factor = * 1
    temp = s32floatfactor(value[20:24],0.001)
    Values.append(temp)
    ValuesAsText.append("light             -Value : {0} lux : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} lux : light".format(substrpad(str(temp),10," ")))
    #24-25 magnetometerRaw_x int16_t LSB/µT - convert factor = * 16
    temp = s16floatdiv(value[24:26],16)
    Values.append(temp)
    ValuesAsText.append("magnetometerRaw_x -Value : {0} µT : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} µT : magnetometerRaw_x".format(substrpad(str(temp),10," ")))
    #26-27 magnetometerRaw_y int16_t LSB/µT - convert factor = * 16
    temp = s16floatdiv(value[26:28],16)
    Values.append(temp)
    ValuesAsText.append("magnetometerRaw_y -Value : {0} µT : ".format(substrpad(str(temp),10," ")))
    print("-Value : {0} µT : magnetometerRaw_y".format(substrpad(str(temp),10," ")))
    #28-29 magnetometerRaw_z int16_t LSB/µT - convert factor = * 16
    temp = s16floatdiv(value[28:30],16)
    Values.append(temp)
    ValuesAsText.append("magnetometerRaw_z -Value : {0} µT : ".format(substrpad(str(temp),10," "))) 
    print("-Value : {0} µT : magnetometerRaw_z".format(substrpad(str(temp),10," ")))   
    #30-31 thresholdviolation int16_t bit mask
    print("Value : {0:b} : {1}".format(int.from_bytes(value[30:32],byteorder="big"),"thresholdViolation"))
    Values.append(int.from_bytes(value[30:32],byteorder="big"))
    ValuesAsText.append("Value : {0:b} : {1}".format(int.from_bytes(value[30:32],byteorder="big"),"thresholdViolation"))
    #32 rollingCounter int8_t 
    short_("rollingCounter",value[32])
    Values.append(value[32])
    ValuesAsText.append("rollingCounter : {0}".format(value[32]))

