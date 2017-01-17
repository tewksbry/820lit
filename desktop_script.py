import random
import itertools
from visualizer import Visualizer
import pattern
import sound_visualizer
import pyaudio
import numpy as np

last_volume = 0
PIXEL_NUM = 240


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
    stream = sound_visualizer.p.open(format=pyaudio.paInt16,
                                     channels=sound_visualizer.CHANNELS,
                                     rate=sound_visualizer.RATE,
                                     frames_per_buffer=sound_visualizer.CHUNK,
                                     input=True,
                                     stream_callback=sound_callback)

    stream.start_stream()

    while stream.is_active():
        visualizer.update(
            pattern.middleOutRainbowPatternFromVolume(last_volume, PIXEL_NUM))
        visualizer.checkClosure()

    stream.stop_stream()

    stream.close()

    visualizer.p.terminate()


main()
