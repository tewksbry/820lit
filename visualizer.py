import pygame
from pygame.locals import *
import pattern
import serial
import time
import sys


class Visualizer:
    """docstring for Visualizer"""

    def __init__(self, pixels=240, displayWidth=1300, displayHeight=100, pixelWidth=5, pixelHeight=50, patternSet=pattern.defaultPatternSet()):
        self.pixels = pixels
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        self.pixelRGBW = [(0, 0, 0, 0) for _ in range(pixels)]
        self.patternSet = patternSet

        pygame.init()
        self.display = pygame.display.set_mode(
            (displayWidth, displayHeight), 0, 32)
        self.display.fill((255, 255, 255))

        self.arduinoConnected = True

        try:
            self.ser = serial.Serial('/dev/tty.usbserial', 9600)
        except Exception as e:
            print "Serial connection error: ", e.args
            self.arduinoConnected = False

    def update(self, pattern=None):
        if not pattern:
            pattern = self.pattern.next()
        for i in range(self.pixels):
            left = (self.displayWidth - self.pixels *
                    self.pixelWidth) / 2 + i * self.pixelWidth
            top = (self.displayHeight - self.pixelHeight) / 2

            pygame.draw.rect(self.display, pattern.arr[i].RGB(
            ), (left, top, self.pixelWidth, self.pixelHeight))
        pygame.display.update()
        if self.arduinoConnected:
            ba = bytearray(list(itertools.chain.from_iterable(pixelRGBW)))
            self.ser.write(ba)

    def play(self, patternSet=None, delay=0):
        if pattern is not None:
            self.pattern = pattern
        while True:
            self.checkClosure()
            time.sleep(delay / 1000.0)
            self.update()

    def checkClosure(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
