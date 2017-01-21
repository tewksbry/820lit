#!/usr/bin/python
import struct
import serial
import time


class NeoPixel(object):
    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbmodem1451', 115200, timeout=0)
        self.command_count = 0
        self.command = ""

    def setPixelColor(self, pixel, red, green, blue, white):
        # message = struct.pack('>BBBHBBBB', ord(':'), self.command_count, ord('c'), pixel, red, green, blue, white)
        message = struct.pack('>BBBBBBB', ord(':'), ord('c'), pixel, red, green, blue, white)
        # print message
        # self.command_count += 1
        # if self.command_count >= 255:
        #     self.command_count = 0
        # print(message)
        # self.ser.write(message)
        if self.command == "":
            self.command = message
        else:
            self.command += message
        # response = self.ser.readline()
        # print(response)

    def show(self):
        # message = struct.pack('BBB', ord(':'), self.command_count, ord('s'))
        message = struct.pack('BB', ord(':'), ord('s'))
        # self.command_count += 1
        # print(message)
        # self.ser.write(message)
        if self.command == "":
            self.command = message
        else:
            self.command += message
        # response = self.ser.readline()
        # print(response)

    def send(self):
        # print "COMMAND", self.command
        # try:
        self.ser.write(self.command)
        # time.sleep(0.2)
        # except Exception as e:
        #     print e.message
        self.command = ""


if __name__ == "__main__":

    strand = NeoPixel()

    strand.setPixelColor(0, 255, 0, 0, 0)
    strand.show()
    strand.send()
    time.sleep(1)
    strand.setPixelColor(0, 0, 255, 0, 0)
    strand.setPixelColor(1, 255, 0, 0, 0)
    strand.show()
    strand.send()
    time.sleep(1)
    strand.setPixelColor(0, 0, 0, 255, 0)
    strand.setPixelColor(1, 0, 255, 0, 0)
    strand.setPixelColor(2, 255, 0, 0, 0)
    strand.show()
    strand.send()
    time.sleep(1)
    strand.setPixelColor(0, 0, 0, 0, 255)
    strand.setPixelColor(1, 0, 0, 255, 0)
    strand.setPixelColor(2, 0, 255, 0, 0)
    strand.show()
    strand.send()
    time.sleep(1)
    strand.setPixelColor(0, 0, 0, 0, 0)
    strand.setPixelColor(1, 0, 0, 0, 255)
    strand.setPixelColor(2, 0, 0, 255, 0)
    strand.show()
    strand.send()
    time.sleep(1)
    strand.setPixelColor(0, 0, 0, 0, 0)
    strand.setPixelColor(1, 0, 0, 0, 0)
    strand.setPixelColor(2, 0, 0, 0, 255)
    strand.show()
    strand.send()
