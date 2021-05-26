from __main__ import *
import serial
import time
import os
global y
ser = serial.Serial(
        #port='/dev/serial0',
        port='/dev/ttyS0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
# IMPORTANT!!!
# The device uses little endian format

# first 3 parts of Data Packet. Sum is 100. Chances are i won't need this
stddp = [
    0x5a,       # Data start code1
    0xa5,       # Data start code2
    0x01, 0x00  # Device ID
]

#turn true if you want to see all data
debugging = True

def CalculateCheckSum(self,bytearr):
        return sum(map(ord,bytes(bytearr)))


def recieve(bytenum, imgfilename = "Image", store = False):
    basic = [0] * 8
    #responce = [] 
    
    for i in range(0, 4):
        basic[i] = ser.read(1)
        if debugging:
            print (basic)
    if store:
        print ("begining with the data gathering")
        with open("image",'ab') as f:
            for i in range(0, bytenum):
                byte = ser.read(1)
                f.write(byte)
                print(str(i) + ": " + str(int.from_bytes(byte, byteorder="little")))
        f.close()
    #if debugging:
    #    print(responce)
    print(ser.read(2))


# Accepts a binary number and breaks it apart and returns them in form of a string
def bytestostring(num):
    broke = [0] * 6
    num = int.from_bytes(num, byteorder="little")
    broke[0] = hex(num & 0xff)              # Response start code 1
    num = num >> 8
    broke[1] = hex(num & 0xff)              # Response start code 2
    num = num >> 8
    broke[2] = hex(num & 0xffff)            # Device id
    num = num >> 16
    broke[3] = hex(num & 0xffffffff)        # parameters
    num = num >> 32
    broke[4] = hex(num & 0xffff)            # command code
    num = num >> 16
    broke[5] = hex(num & 0xffff)            # check sum
    return broke

# Open command is used to initialize the device; especially it gets device's static info
# Info is either 0x01 or 0x00 (default)
def _open(info = 0x00):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x01, 0x00,
        0x01, 0x01
    ]))
    if debugging == True:
        print(bytestostring(ser.read(12)))
    else:
        ser.read(12)
    if  info != 0x00:
        ser.read(4)

        print("Firmware Version:\t\t" + str(int.from_bytes(ser.read(4), byteorder="little")))
        print("Iso Area Max Size:\t\t" + str(int.from_bytes(ser.read(4), byteorder="little")))
        print("Device Serial Number:\t" + hex(int.from_bytes(ser.read(16), byteorder= "little")))
        if int.from_bytes(ser.read(1), byteorder="little") != 13:
            print("there was an issue with initialization data packet sum")
            return 0
        else:
            return 1
    else:
        return 1

# Led lamp, off (0x00) by default
def cmosled(x = 0x00):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00 + x, 0x00, 0x00, 0x00,
        0x12, 0x00,
        0x12 +x, 0x01
    ]))
    x = bytestostring(ser.read(12))
    if debugging == True:
        print(x)
    if x[4] == "0x30":
        print("Cmosled works")
    else:
        print("cmosled doesn't work")


def changebaudrate():
    if ser.baudrate == 9600:
        ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0xc2, 0x01, 0x00,
        0x04, 0x00,
        0xc7, 0x01
        ]))
        #ser.baudrate = 115200
    else:
        ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x80, 0x25, 0x00, 0x00,
        0x04, 0x00,
        0xA9, 0x01
        ]))
        #ser.baudrate = 9600
    print(bytestostring(ser.read(12)))


def getenrollcount():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x20, 0x00,
        0x20, 0x01
    ]))

    print(bytestostring(ser.read(12)))


def enrollstart(ID = 0x00):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        ID,   0x00, 0x00, 0x00,
        0x22, 0x00,
        0x22 + ID,  0x01
    ]))
    time.sleep(2)
    x = bytestostring(ser.read(12))
#    if debugging == True:
#        print(x)
    if x[3] == "0x1009":
        print("Database is full")
        return 0
    elif x[3] == "0x1003":
        print("The spesified ID is not between 0~19")
        return 1
    elif x[3] == "0x1005":
        print("The specified ID is already used")
        return 2
    else:
        print("Enrollstart Done")
        return 3


# returns True for success and False for failure
def enroll1():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x23, 0x00,
        0x23, 0x01
    ]))
    x = bytestostring(ser.read(12))
#    if debugging == True:
#        print(x)
    if x[3] == "0x100c":
        print("Too bad fingerprint")
        return False
    elif x[3] == "0x100d":
        print("Enrollment Failure")
        return False
    else:
        print("Enroll 1: Successful")
        return True

# returns True for success and False for failure
def enroll2():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x24, 0x00,
        0x24, 0x01
    ]))
    x = bytestostring(ser.read(12))
#    if debugging == True:
#        print(x)
    if x[3] == "0x100c":
        print("Too bad fingerprint")
        return False
    elif x[3] == "0x100d":
        print("Enrollment Failure")
        return False
    else:
        print("Enroll 2: Successful")
        return True

# returns True for success and False for failure
def enroll3():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x25, 0x00,
        0x25, 0x01
    ]))
    x = bytestostring(ser.read(12))
#    if debugging == True:
#        print(x)
    if x[3] == "0x100c":
        print("Bad fingerprint")
        return False
    elif x[3] == "0x100d":
        print("Enrollment Failure")
        return False
    else:
        print("Enroll 3: Successful")
        return True



def ispressfinger():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x26, 0x00,
        0x26, 0x01
    ]))
    x = bytestostring(ser.read(12))
#    print(x)
    if x[0] == "0x0":
        return 3
    if x[3] == "0x0":
        return True
    else:
        return False


def deleteid(x = 0):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00 + x, 0x00, 0x00, 0x00,
        0x40, 0x00,
        0x40 + x, 0x01
    ]))
    x = bytestostring(ser.read(12))
    if debugging:
        if x[3] == "0x1003":
            print("The spesified ID is not between 0~19")
        else:
            print("The id deleted")


def deleteall():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x41, 0x00,
        0x41, 0x01
    ]))
    x = bytestostring(ser.read(12))
    if debugging:
        if x[3] == "0x100a":
            print("Database is empty")
        else:
            print("All ids deleted")


def verify(x = 0x00):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00 + x, 0x00, 0x00, 0x00,
        0x50, 0x00,
        0x50 +x, 0x01
    ]))
    time.sleep(1.5)
    x = bytestostring(ser.read(12))
    if debugging:
        if x[3] == "0x1003":
            print("The spesified ID is not between 0~19")
            return -2
        elif x[3]== "0x1004":
            print("The specified ID is not used")
            return -1
        elif x[3] == "0x1007":
            print("1:1 Verification Failure")
            return 0
        else:
            print("Successful verification")
            return 2


def identify():
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x51, 0x00,
        0x51, 0x01
    ]))
    x = bytestostring(ser.read(12))
    print(x)
    if x[3] == "0x100a":
        print("Database is empty")
        return 2
    elif x[3] == "0x1008":
        print("1:N Identification Failure")
        return 3
    else:
        print("Successful identification")
        return (x[3])


def capturefinger(x = 0x00):
    ser.write(bytearray([
        0x55,
        0xaa,
        0x01, 0x00,
        0x00 + x, 0x00, 0x00, 0x00,
        0x60, 0x00,
        0x60 + x, 0x01
    ]))
    x = bytestostring(ser.read(12))
    if x[3] == "0x1012":
        print("Finger is not pressed")
        return False
    else:
        return True


