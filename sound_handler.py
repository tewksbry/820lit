# Author: Samuel Resendez

import pyaudio

import numpy as np
import math


"""
soundHandler class, for Neil's IoT Thing
"""


class soundHandler(object):
    """pyDocs here"""

    def __init__(self, channel_number=1, rate=44100, chunk=512):
        """Initializes a soundHandler, with default values that provide 60 readings per second, scaled to output 0 - 100.
        Can be updated to set the channel_number, rate, and chunk

        channel_number: Int
        rate : Int
        chunk : Int

        """

        self.__CHANNELS = channel_number
        self.__RATE = rate
        self.__CHUNK = chunk
        self.__max_output = 100
        self.__dependency = -0.0099
        self.__scale_factor = 50
        self.stream = None
        self.__currPattern = 0
        self.__isActive = False
        self.data_tuple = [0, 0, 0]
        # self.queue = Queue.Queue()

    def close_stream(self):
        if self.__isActive:
            self.__isActive = False
        else:
            pass

    def __sigmoid(self, x):
        """Math function which maps values to set volume scale"""

        volume = round(self.__max_output / (1 + self.__scale_factor * math.exp(self.__dependency * x)))
        if int(volume) == 2:
            volume = 0
        return volume

    def __update_curr_pattern(self, response):
        if response.raw_body.isdigit():
            self.__currPattern = int(response.raw_body)

    def __frequencySigmoid(self, freq):
        return round(100 / (1 + 10 * math.exp(-0.0003 * freq)))

    def update_sigmoid_params(self, max_value=100, input_dependency=-0.0003, scale_factor=8):
        """Can update the values of the sigmoid function, if needed"""
        self.__max_output = max_value
        self.__dependency = input_dependency
        self.__scale_factor = scale_factor

    def is_active(self):
        return self.stream.is_active

    def __callback(self, in_data, frame_count, time_info, flag):
        """Private function used to interface with pyAudio"""
        audio_data = np.fromstring(in_data, dtype=np.int16)

        # if int(frame_count) % 2 == 0:
        #   url = "https://sound-visualizer-6443f.firebaseio.com/PatternID.json"
        #    unirest.get(url, callback=self.__update_curr_pattern)
        print(audio_data)
        raw_val = max(audio_data) - 25
        if raw_val < 0:
            raw_val = 0

        # do processing here
        print("Volume raw input: " + str(raw_val))
        last_volume = self.__sigmoid(raw_val)
        print("Volume input: " + str(last_volume))
        # Do the calculations
        fftData = abs(np.fft.rfft(audio_data)) ** 2
        which = fftData[1:].argmax() + 1

        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            frequency = (which + x1) * self.__RATE / self.__CHUNK
        else:
            frequency = which * self.__RATE / self.__CHUNK

        self.data_tuple = [last_volume, frequency, self.__currPattern]
        # self.queue.put((last_volume,frequency,self.__currPattern))

        if self.__isActive:
            return (audio_data, pyaudio.paContinue)
        else:
            return (audio_data, pyaudio.paAbort)

    def start_stream(self, callback_function):
        """Starts stream, and reads volumes values into the callback function for processing
        Callback takes one argument, which is the numeric volume data as an Integer"""
        self.__isActive = True

        self.__handle_volume_data = callback_function

        p = pyaudio.PyAudio()
        device_index = 0
        for x in range(p.get_device_count()):
            if p.get_device_info_by_index(x)["maxInputChannels"] > 0:
                device_index = x
                break

        for x in range(p.get_device_count()):
            if p.get_device_info_by_index(x)["name"] == u'Soundflower (2ch)':
                device_index = x

        self.stream = p.open(format=pyaudio.paInt16,
                             channels=self.__CHANNELS,
                             rate=self.__RATE,
                             frames_per_buffer=self.__CHUNK,
                             input=True,
                             stream_callback=self.__callback,
                             input_device_index=device_index)

        self.stream.start_stream()

        while self.stream.is_active():
            self.__handle_volume_data(self.data_tuple[0], self.data_tuple[1], self.data_tuple[2])

        print("Closing PyAudio Stream...")
        self.stream.close()
        print("PyAudio stream closed.")

# ----- just for testing purposes ----- #


def main():

    handler = soundHandler()

    def callback(volume, frequency, pattern):
        pass

        # return volume

    handler.start_stream(callback_function=callback)


if __name__ == "__main__":

    main()
