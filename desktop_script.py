from visualizer import Visualizer
from pattern import Pattern
from pattern import LED
import pattern
import sound_visualizer
import pyaudio
import numpy as np
from sound_handler import soundHandler
import time

PIXEL_NUM = 240
next_pattern = Pattern([LED() for _ in range(PIXEL_NUM)])
last_volume = 0


def normalize_frequency(f):
    f = 100 * f / 3000
    if f > 100:
        f = 100
    return int(f)


def patternCreator(volume=0, frequency=0, patternNum=0):
    patternNum = int(patternNum)
    the_pattern = pattern.raindowColors
    if patternNum in (1, 2, 3, 4):
        the_pattern = pattern.raindowColors
    elif patternNum in (5, 6, 7, 8):
        the_pattern = pattern.rotatedRainbow
    elif patternNum in (9, 10, 11):
        the_pattern = pattern.grayScale
    elif patternNum in (12, 13, 14):
        the_pattern = pattern.redToWhite
    elif patternNum in (15, 16, 17):
        the_pattern = pattern.blueToWhite
    elif patternNum in (18, 19, 20):
        the_pattern = pattern.greenToWhite

    if patternNum in (1, 5, 9, 12, 15, 18):
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=the_pattern, last_volume=last_volume)
    elif patternNum in (2, 6, 10, 13, 16, 19):
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=0.7, fill=False, color_palette=the_pattern, last_volume=last_volume)
    elif patternNum in (3, 7, 11, 14, 17, 20):
        frequencyColor = the_pattern[int(len(the_pattern) * normalize_frequency(frequency) / 100.0) - 1]
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=[frequencyColor], last_volume=last_volume)
    elif patternNum in (4, 8):
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=True, color_palette=the_pattern, last_volume=last_volume)
    elif patternNum == 0:
        time.sleep(0.1)
        return pattern.sparkle()

    frequencyColor = pattern.raindowColors[int(len(pattern.raindowColors) * frequency / 100.0) - 1]
    return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=[frequencyColor], last_volume=last_volume)
    # return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=pattern.rotatedRainbow, last_volume=last_volume)


def sound_callback(in_data, frame_count, time_info, flag):
    global last_volume
    audio_data = np.fromstring(in_data, dtype=np.int16)
    # do processing here
    last_volume = sound_visualizer.sigmoid(max(audio_data))

    return (audio_data, pyaudio.paContinue)


def main():
    # visualizer = Visualizer(pattern=pattern.rainbow())
    # visualizer.play(delay=0)

    visualizer = Visualizer()
    handler = soundHandler()

    def new_pattern(volume, frequency, pattern):
        global last_volume

        next_pattern = patternCreator(volume=volume, frequency=frequency, patternNum=pattern)
        last_volume = volume
        visualizer.update(next_pattern)
        visualizer.checkClosure()
        return volume

    handler.start_stream(callback_function=new_pattern)


main()
