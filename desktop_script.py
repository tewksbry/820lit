from visualizer import Visualizer
from pattern import Pattern
import pattern
import sound_visualizer
import pyaudio
import numpy as np
from sound_handler import soundHandler


PIXEL_NUM = 240
next_pattern = Pattern()
last_volume = 0


def patternCreator(volume=0):
    return pattern.middleOut(volume, previous=next_pattern, fade=0.95, cutoff=0.75, fill=False, colorPattern=pattern.rotatedRainbow, lastVolume=last_volume)


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
        global last_volume
        next_pattern = patternCreator(volume=volume)
        last_volume = volume
        visualizer.update(next_pattern)

        visualizer.checkClosure()
        return volume

    handler.start_stream(callback_function=new_pattern)


main()
