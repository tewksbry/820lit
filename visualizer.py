import pygame
from pygame.locals import *
import pattern
import serial
import time
import sys
import itertools
import struct
import neopixel
import datetime


class Visualizer:
    """docstring for Visualizer"""

    def __init__(self, pixels=240, displayWidth=1440, displayHeight=50, pixelWidth=6, pixelHeight=50, patternSet=pattern.defaultPatternSet()):
        self.pixels = pixels
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        self.pixelRGBW = [(0, 0, 0, 0) for _ in range(pixels)]
        self.patternSet = patternSet
        self.strand = neopixel.NeoPixel()

        pygame.init()
        self.display = pygame.display.set_mode(
            (displayWidth, displayHeight), 0, 32)
        self.display.fill((255, 255, 255))

        self.arduinoConnected = True

        # try:
        #     self.ser = serial.Serial('/dev/tty.usbmodem1451', 9600)
        # except Exception as e:
        #     print "Serial connection error: ", e.args
        #     self.arduinoConnected = False

    def update(self, pattern=None):
        start = datetime.datetime.now()
        if not pattern:
            pattern = self.patternSet.next()
        for i in range(self.pixels):
            left = (self.displayWidth - self.pixels *
                    self.pixelWidth) / 2 + i * self.pixelWidth
            top = (self.displayHeight - self.pixelHeight) / 2

            pygame.draw.rect(self.display, pattern.arr[i].RGB(
            ), (left, top, self.pixelWidth, self.pixelHeight))
            # self.strand.setPixelColor(i, *pattern.arr[i].RGBW())
            # self.strand.send()
            # self.strand.show()
            # self.strand.send()
            # time.sleep(0.1)

        # self.strand.show()
        self.strand.setPixelArray(pattern)
        self.strand.send()
        pygame.display.update()
        end = datetime.datetime.now()
        millis = int((end - start).total_seconds() * 1000)
        print 1000 / millis, "fps"

        # # if self.arduinoConnected:
        #     # pass
        #     # l = list(itertools.chain.from_iterable(map(lambda x: x.RGBW(), pattern.arr)))
        #     # ba = bytearray(l)
        #     # ba = bytearray([255, 255, 255, 255] * 240)
        #     # print "l", l
        #     # lis = list(itertools.chain.from_iterable([(255, 255, 255, 255)] * 240))
        #     # b = struct.pack('>' + 'B' * 960, *lis)
        #     print "hello"
        #     # r = [bytes(65)] * 960
        #     for LED in pattern.arr:
        #         RGBW = LED.RGBW()
        #         # self.ser.write(bytes(RGBW[0]))
        #         # self.ser.write(bytes(RGBW[1]))
        #         # self.ser.write(bytes(RGBW[2]))
        #         # self.ser.write(bytes(0))
        #         self.ser.write(bytes(255))
        #         self.ser.write(bytes(0))
        #         self.ser.write(bytes(0))
        #         self.ser.write(bytes(0))

        #     # print "output", str(self.ser.read())

    def play(self, patternSet=None, delay=0):
        if patternSet is not None:
            self.patternSet = patternSet
        while True:
            self.checkClosure()
            time.sleep(delay / 1000.0)
            self.update()

    def checkClosure(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
