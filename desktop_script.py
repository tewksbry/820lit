import random
import itertools
from visualizer import Visualizer
from pattern import Pattern
from pattern import PatternSet
import pattern
import sound_visualizer
import pyaudio
import numpy as np
from sound_handler import soundHandler
import Queue


last_volume = 0
PIXEL_NUM = 240
last_pattern = Pattern()


def sound_callback(in_data, frame_count, time_info, flag):
    global last_volume
    audio_data = np.fromstring(in_data, dtype=np.int16)
    # do processing here
    last_volume = sound_visualizer.sigmoid(max(audio_data))

    return (audio_data, pyaudio.paContinue)


def main():
    # visualizer = Visualizer(pattern=pattern.rainbow())
    # visualizer.play(delay=0)
    global last_pattern
    visualizer = Visualizer()

    handler = soundHandler()

    def new_pattern(volume, prev_pattern=last_pattern):
        new_patt = pattern.middleOutWithEndsRainbowPatternFromVolume(
            volume, PIXEL_NUM, previous=prev_pattern)
        visualizer.update(new_patt)

        visualizer.checkClosure()
        return volume

    handler.start_stream(callback_function=new_pattern)



main()
