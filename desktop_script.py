from sound_handler import soundHandler
import serial
import struct
import time
import sys
import queue
import threading


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
    # print ":" + name + " " + " ".join(map(str, argv))
    ser.write(struct.pack('>BB', ord(':'), ord(name)))
    for arg in argv:
        ser.write(struct.pack('>B', arg))
        time.sleep(0.01)
    # print "BB:", bb
    # ser.write(bb)


def main():

    port = '/dev/tty.usbmodem1451'
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    ser = serial.Serial(port, 115200)
    handler = soundHandler()
    cmd_queue = queue.Queue()

    def checkForInput():
        while(not cmd_queue.empty()):
            cmd = cmd_queue.get()
            if len(cmd) < 1:
                return
            args = cmd.split()
            print args
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
                ser.close()
                sys.exit(0)

    def command(queue):
        while (True):
            inp = raw_input()
            queue.put(inp)
            if inp == "exit":
                break

    def new_pattern(volume, frequency, patt):
        ser.readline()
        passParam(ser, 'v', volume)
        passParam(ser, 'f', normalize_frequency(frequency))
        # time.sleep(0.1)
        # command(cmd_queue)
        checkForInput()
        # print "v", volume
        # print "f", normalize_frequency(frequency)
        ser.reset_output_buffer()
        return volume

    commands = threading.Thread(target=command, args=(cmd_queue,))
    commands.start()
    handler.start_stream(callback_function=new_pattern)


main()
