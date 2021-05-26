import fingerprint
import time

def enroll(quality = 0x00, ID = 0x00):
    print("Begining enrollment at ID")
    fingerprint.cmosled(1)
    print("LED is on")
    time.sleep(2)
    print("Preparing for Enrollment")
    if fingerprint.enrollstart(ID) == 3:
        while True:
            print("Press and hold your finger for enrollment 1")
            while not fingerprint.capturefinger(quality):
                time.sleep(1)
            if fingerprint.enroll1():
                time.sleep(1)
                break
       	print("Remove your finger")
        while fingerprint.ispressfinger():
            time.sleep(1)
        while True:
            print("Press and hold your finger for enrollment 2")
            while not fingerprint.capturefinger(quality):
                time.sleep(1)
            if fingerprint.enroll2():
                time.sleep(1)
                break
        print("Remove your finger")
        while fingerprint.ispressfinger():
            pass
        while True:
            print("Press and hold your finger for enrollment 3")
            while not fingerprint.capturefinger(quality):
                time.sleep(1)
            if fingerprint.enroll3():
                time.sleep(1)
                break
        fingerprint.cmosled()
        return 2
    else:
        return 0 
        print("error")


def delete(pos):
    fingerprint.deleteid(pos)

def deleteall():
    fingerprint.deleteall()

def capture(quality = 0x00):
    if fingerprint.ispressfinger():
        while fingerprint.ispressfinger():
            print("Remove your finger from the scanner.")
    else:
        while not fingerprint.ispressfinger():
            print("Put your finger on the scanner.")
    if fingerprint.capturefinger(quality):
        time.sleep(1)
    else:
        print("There has been a failure with image capturing")
        fingerprint.cmosled()
        exit()

    
