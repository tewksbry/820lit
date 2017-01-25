from sound_handler import soundHandler
import serial
import struct
import time
import sys
import queue


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


def passParam(ser, name, *argv):
    print ":" + name + " " + " ".join(map(str, argv))
    print "arg length", len(argv)
    ser.write(struct.pack('>BB', ord(':'), ord(name)))
    for arg in argv:
        time.sleep(0.01)
        ser.write(struct.pack('>B', arg))
    # print "BB:", bb
    # ser.write(bb)


def main():

    port = '/dev/tty.usbmodem1451'
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    ser = serial.Serial(port, 9600, writeTimeout=0)
    handler = soundHandler()
    cmd_queue = queue.Queue()

    def checkForInput():
        while(not cmd_queue.empty()):
            cmd = cmd_queue.get()
            if len(cmd) < 1:
                return
            args = cmd.split()

            time.sleep(0.1)
            if args[0] == 'p' or args[0] == "palette":
                passParam(ser, 'p', int(args[1]))
            elif args[0] == 'a' or args[0] == 'fade':
                passParam(ser, 'a', int(float(args[1]) * 100))
            elif args[0] == 'c' or args[0] == 'cutoff':
                passParam(ser, 'v', int(float(args[1]) * 100))
            elif args[0] == 'd' or args[0] == 'display':
                passParam(ser, 'd', int(args[1]))
            elif args[0] == 'l' or args[0] == 'light':
                passParam(ser, 'l', *map(int, args[1:]))
            elif args[0] == 'b' or args[0] == 'brightness':
                passParam(ser, 'l', *map(int, args[1:]))
            elif args[0] == 's' or args[0] == 'dimcenter':
                passParam(ser, 's', int(args[1]))
            elif args[0] == 'e' or args[0] == 'brightedges':
                passParam(ser, 'e', int(args[1]))
            elif args[0] == 'exit':
                sys.exit(0)
            time.sleep(0.1)

    def command(queue):
        inp = raw_input()
        queue.put(inp)

    def new_pattern(volume, frequency, patt):
        # passParam(ser, 'v', volume)
        # passParam(ser, 'f', normalize_frequency(frequency))
        command(cmd_queue)
        checkForInput()
        print "v", volume
        print "f", normalize_frequency(frequency)
        return volume

    handler.start_stream(callback_function=new_pattern)


main()
