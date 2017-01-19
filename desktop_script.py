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


def patternCreator(volume=0, frequency=0, patternNum=0):
    patternNum = int(patternNum)
    if patternNum == 1:
        frequencyColor = pattern.raindowColors[int(len(pattern.raindowColors) * frequency / 100.0) - 1]
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=[frequencyColor], last_volume=last_volume)
    elif patternNum == 2:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=pattern.rotatedRainbow, last_volume=last_volume)
    elif patternNum == 3:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=0.7, fill=False, color_palette=pattern.rotatedRainbow, last_volume=last_volume)
    elif patternNum == 4:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=pattern.raindowColors, last_volume=last_volume)
    elif patternNum == 5:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=True, color_palette=pattern.raindowColors, last_volume=last_volume)
    elif patternNum == 6:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=0.7, fill=False, color_palette=pattern.raindowColors, last_volume=last_volume)
    elif patternNum == 7:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=1, fill=False, color_palette=pattern.grayScale, last_volume=last_volume)
    elif patternNum == 8:
        return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=0.8, fill=False, color_palette=pattern.grayScale, last_volume=last_volume)
    elif patternNum == 9:
        # time.sleep(0.1)
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
    # while True:
    #     visualizer.update(pattern.sparkle())

    #     visualizer.checkClosure()
    #     time.sleep(0.1)
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
