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
    ser.write(struct.pack('>BB', ord(':'), ord(name)))
    for arg in argv:
        ser.write(struct.pack('>B', arg))
        time.sleep(0.01)


def main():

    port = '/dev/tty.usbmodem1451'
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    ser = None
    ser = serial.Serial(port, 115200)
    handler = soundHandler()
    cmd_queue = queue.Queue()
    cmd_dict = {}

    def checkForInput():
        while(not cmd_queue.empty()):
            cmd = cmd_queue.get()
            if len(cmd) < 1:
                continue
            args = cmd.split()
            cmd_dict[args[0]] = args[1:]

        for key, value in cmd_dict.iteritems():
            if key == '-p' or key == "--palette":
                passParam(ser, 'p', int(value[0]))
            elif key == '-a' or key == '--fade':
                passParam(ser, 'a', int(float(value[0]) * 100))
            elif key == '-c' or key == '--cutoff':
                passParam(ser, 'c', int(float(value[0]) * 100))
            elif key == '-d' or key == '--display':
                passParam(ser, 'd', int(value[0]))
            elif key == '-l' or key == '--light':
                passParam(ser, 'l', *map(int, value))
            elif key == '-b' or key == '--brightness':
                passParam(ser, 'b', int(value[0]))
            elif key == '-s' or key == '--dimcenter':
                passParam(ser, 's', int(value[0]))
            elif key == '-e' or key == '--brightedges':
                passParam(ser, 'e', int(value[0]))
            elif key == '-exit':
                ser.close()
                sys.exit(0)
            elif key == '-h' or key == '--help':
                print "Availible commands:"
                print "Palette number: -p [num]"
                print "Display type number: -d [num]"
                print "Fade rate: -a [0 - 1]"
                print "Cutoff: -c [0 - 1]"
                print "Single light color: -l [R] [G] [B] [W]"
                print "Brightness: -b [0 - 255]"
                print "Dim center: -s [0 or 1]"
                print "Brighten edges: -e [0 or 1]"
        cmd_dict.clear()

    def command(queue):
        while (True):
            inp = raw_input()
            queue.put(inp)
            if inp == "-exit":
                break

    def new_pattern(volume, frequency, patt):
        ser.readline()
        passParam(ser, 'v', volume)
        passParam(ser, 'f', normalize_frequency(frequency))
        checkForInput()
        # ser.reset_output_buffer()
        return volume

    commands = threading.Thread(target=command, args=(cmd_queue,))
    commands.start()
    handler.start_stream(callback_function=new_pattern)


main()
