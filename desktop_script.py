from sound_handler import soundHandler
import serial
import struct
import time
import sys
import Queue
import threading
import unirest
import json


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

    port = '/dev/tty.usbmodem1461'
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    ser = None
    ser = serial.Serial(port, 115200)
    handler = soundHandler()
    cmd_queue = Queue.Queue()
    cmd_dict = {}
    param_dict = {}
    url = "https://sound-visualizer-6443f.firebaseio.com/.json"

    def request_callback(response):
        params = json.loads(response.raw_body)

        # Pattern
        cmd_queue.put(["-p", params[u'PatternID']])

        # Brightness
        cmd_queue.put(["-b", params[u'brightness']])

        # Light color
        cmd_queue.put(["-l", params[u'R'], params[u'G'], params[u'B'], params[u'W']])

        # Cycle speed
        cmd_queue.put(["-y", params[u'cycleSpeed']])

        # Fade amount
        cmd_queue.put(["-a", params[u'Fade']])

    def setParam(key, value):
        if key not in param_dict or param_dict[key] != value:
            print "Updating parameters"
            passParam(ser, key, *value)
            param_dict[key] = value
            print "New parameters:", param_dict

    def checkForInput():
        while(not cmd_queue.empty()):
            args = cmd_queue.get()
            cmd_dict[args[0]] = args[1:]

        for key, value in cmd_dict.iteritems():
            if key == '-p' or key == "--palette":
                setParam('p', [int(value[0])])
            elif key == '-a' or key == '--fade':
                setParam('a', [int(float(value[0]) * 100)])
            elif key == '-c' or key == '--cutoff':
                setParam('c', [int(float(value[0]) * 100)])
            elif key == '-d' or key == '--display':
                setParam('d', [int(value[0])])
            elif key == '-l' or key == '--light':
                setParam('l', map(int, value))
            elif key == '-b' or key == '--brightness':
                setParam('b', [int(value[0])])
            elif key == '-s' or key == '--dimcenter':
                setParam('s', [int(value[0])])
            elif key == '-e' or key == '--brightedges':
                setParam('e', [int(value[0])])
            elif key == '-y' or key == '--cyclespeed':
                setParam('y', [int(value[0])])
            elif key == '-exit':
                ser.close()
                sys.exit(0)
            elif key == '-h' or key == '--help':
                print "Availible commands:"
                print "Palette number: -p (--palette) [num]"
                print "Display type number: -d (--display) [num]"
                print "Fade rate: -a (--fade) [0 - 1]"
                print "Cutoff: -c (--cutoff) [0 - 1]"
                print "Single light color: -l (--light) [R] [G] [B] [W]"
                print "Brightness: -b (--brightness) [0 - 255]"
                print "Dim center: -s (--dimcenter) [0 or 1]"
                print "Brighten edges: -e (--brightedges) [0 or 1]"
                print "Cycle speed: -y (--cyclespeed) [1 - 255]"

                print "Exit: -exit"
        cmd_dict.clear()

    def command(queue):
        while (True):
            inp = raw_input()
            if len(inp) > 0:
                queue.put(inp.split())
            if inp == "-exit":
                break

    def new_pattern(volume, frequency, patt):
        ser.readline()
        passParam(ser, 'v', volume)
        passParam(ser, 'f', normalize_frequency(frequency))
        checkForInput()
        unirest.get(url, callback=request_callback)
        # ser.reset_output_buffer()
        return volume

    commands = threading.Thread(target=command, args=(cmd_queue,))
    commands.start()

    handler.start_stream(callback_function=new_pattern)


main()
