from sound_handler import soundHandler
import serial
import struct


def normalize_frequency(f):
    if f < 0 or not f:
        return 0
    f = 100 * f / 3000
    if f > 100:
        f = 100
    if f >= 0 and f <= 100:
        return int(f)
    else:
        return 0


def main():
    ser = serial.Serial('/dev/tty.usbmodem1451', 115200, timeout=0)
    handler = soundHandler()

    def new_pattern(volume, frequency, patt):
        # print "v", volume
        # print "f", frequency
        ser.write(struct.pack('>BBB', ord(':'), ord('v'), volume))
        # ser.write(struct.pack('>BBB', ord(':'), ord('f'), normalize_frequency(frequency)))
        return volume

    handler.start_stream(callback_function=new_pattern)


main()
