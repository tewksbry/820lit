from visualizer import Visualizer
from pattern import Pattern
import pattern
import sound_visualizer
import pyaudio
import numpy as np
from sound_handler import soundHandler


PIXEL_NUM = 240
next_pattern = Pattern()


def patternCreator(volume=0):
    # return pattern.middleOutRainbowWithFillPatternFromVolume(volume, PIXEL_NUM)
    return pattern.middleOutWithEndsRainbowPatternFromVolume(volume, PIXEL_NUM, previous=next_pattern, fade=0.95, ending=0.7)


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

    def new_pattern(volume):

        next_pattern = patternCreator(volume=volume)
        visualizer.update(next_pattern)

        visualizer.checkClosure()
        return volume

    handler.start_stream(callback_function=new_pattern)


main()
