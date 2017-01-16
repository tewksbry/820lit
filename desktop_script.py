import serial
import pygame
import sys
import random
import itertools
from pygame.locals import *

numOfPixels = 240
displayWidth = 1300
displayHeight = 100
pixelWidth = 5
pixelHeight = 50
pixelRGBW = [(0, 0, 0, 0) for _ in range(numOfPixels)]
arduinoConnected = True

pygame.init()
display = pygame.display.set_mode((displayWidth, displayHeight), 0, 32)
display.fill((255, 255, 255))

try:
    ser = serial.Serial('/dev/tty.usbserial', 9600)
except Exception as e:
    print "Serial connection error: ", e.args
    arduinoConnected = False


def randomizeColors():
    for i in range(numOfPixels):
        randomColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))
        pixelRGBW[i] = randomColor


def cycleColors():
    for i in range(numOfPixels):
        R = pixelRGBW[i][0] + 1
        G = pixelRGBW[i][1] + 2
        B = pixelRGBW[i][2] + 3
        W = pixelRGBW[i][3] + 4
        if R > 255:
            R = 0
        if G > 255:
            G = 0
        if B > 255:
            B = 0
        if W > 255:
            W = 0
        pixelRGBW[i] = (R, G, B, W)


def convertRGBWtoRGB(RGBW):
    return map(lambda x: (x[0], x[1], x[2]), RGBW)


def updatePixels():
    colors = convertRGBWtoRGB(pixelRGBW)
    for i in range(numOfPixels):
        pygame.draw.rect(display, colors[i], ((displayWidth - numOfPixels * pixelWidth) /
                                              2 + i * pixelWidth, (displayHeight - pixelHeight) / 2, pixelWidth, pixelHeight))


def sendColors():
    ba = bytearray(list(itertools.chain.from_iterable(pixelRGBW)))
    if arduinoConnected:
        ser.write(bytearray(itertools.chain(pixelRGBW)))


def main():

    updatePixels()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        cycleColors()
        updatePixels()
        sendColors()
        pygame.display.update()

main()
