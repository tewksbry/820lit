from sound_handler import soundHandler
import serial
import struct
import time
import sys


def normalize_frequency(f):
    if f < 0 or not f:
        return 0
    f = 100 * f / 2000
    if f > 100:
        f = 100
    if f >= 0 and f <= 100:
        return int(f)
    else:
        return 0


def main():

    port = '/dev/tty.usbmodem1461'
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    ser = serial.Serial(port, 115200, timeout=0)
    handler = soundHandler()

    def new_pattern(volume, frequency, patt):
        # print "v", volume
        # print "f", frequency
        ser.write(struct.pack('>BBB', ord(':'), ord('v'), volume))
        # time.sleep(0.01)
        ser.write(struct.pack('>BBB', ord(':'), ord('f'), normalize_frequency(frequency)))
        # print "v", volume
        # print "f", normalize_frequency(frequency)
        # time.sleep(0.1)
        return volume

    handler.start_stream(callback_function=new_pattern)

main()
