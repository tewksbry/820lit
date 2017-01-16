import serial
import pygame
import sys
import random
import itertools
from pygame.locals import *
import pyrebase

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

config = {
    "apiKey": "AIzaSyCw2VULu88Y6GFyIhA3uX3xH0ELNyGZRX8",
    "authDomain": "sound-visualizer-6443f.firebaseapp.com",
    "databaseURL": "https://sound-visualizer-6443f.firebaseio.com/",
    "storageBucket": "sound-visualizer-6443f.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()
print db.get().val()


def stream_handler(message):
    print(message["event"])  # put
    print(message["path"])  # /-K7yGTTEp7O549EzTYtI
    print(message["data"])  # {'title': 'Pyrebase', "body": "etc..."}
    result = firebase.get('/', None)
    updatePixels()

my_stream = db.stream(stream_handler)

try:
    ser = serial.Serial('/dev/tty.usbserial', 9600)
except Exception as e:
    print "Serial connection error: ", e.args
    arduinoConnected = False


def updateColorsFromServer():
    pass
    # result = firebase.get('/', None)
    # for x in result:
    #     if str(x).isdigit():
    #         pixelRGBW[int(x)] = (result[x][u"R"], result[x][u"G"],
    # result[x][u"B"], result[x][u"W"])


def randomizeColors():
    for i in range(numOfPixels):
        randomColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))
        pixelRGBW[i] = randomColor


def convertRGBWtoRGB(RGBW):
    return map(lambda x: (x[0] + x[3], x[1] + x[3], x[2] + x[3]), RGBW)


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
                my_stream.close()
                pygame.quit()
                sys.exit()
        # updatePixels()
        sendColors()
        pygame.display.update()

main()
