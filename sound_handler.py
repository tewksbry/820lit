#Author: Samuel Resendez

import pyaudio
import time
import numpy as np
import math
import Queue
from matplotlib import pyplot as plt


"""
soundHandler class, for Neil's IoT Thing
"""


class soundHandler(object):
    """pyDocs here"""

    def __init__(self,channel_number=1,rate=8000,chunk=130):

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
        self.__dependency = -0.0003
        self.__scale_factor = 8
        self.stream = None
        self.__input_format = pyaudio.paInt16
        self.__isActive = False
        self.__handle_volume_data
        self.queue = Queue.Queue()



    def __handle_volume_data(self,volume=0): # Should be overridden

        """Internal volume data callback function"""
        print(volume)
        return volume

    def close_stream(self):
        if self.__isActive:
            self.__isActive = False
        else:
            pass


    def __sigmoid(self,x):

        """Math function which maps values to set scale"""

        return int(self.__max_output / (1 + self.__scale_factor * math.exp(self.__dependency * x)))


    def update_sigmoid_params(self,max_value=100,input_dependency=-0.0003,scale_factor=8):

        """Can update the values of the sigmoid function, if needed"""
        self.__max_output = max_value
        self.__dependency = input_dependency
        self.__scale_factor = scale_factor


    def is_active(self):
        return self.stream.is_active

    def  __callback(self,in_data, frame_count, time_info, flag):
        """Private function used to interface with pyAudio"""
        audio_data = np.fromstring(in_data, dtype=np.int16)
        # do processing here
        last_volume = self.__sigmoid(max(audio_data))
        self.queue.put(last_volume)

        if self.__isActive:
            return (audio_data, pyaudio.paContinue)
        else:
            return (audio_data,pyaudio.paAbort)

    def start_stream(self,callback_function=None):
        """Starts stream, and reads volumes values into the callback function for processing
        Callback takes one argument, which is the numeric volume data as an Integer"""
        self.__isActive = True
        if callback_function is not None:
            self.__handle_volume_data = callback_function

        self.stream = pyaudio.PyAudio().open(format=self.__input_format,
                        channels=self.__CHANNELS,
                        rate=self.__RATE,
                        frames_per_buffer=self.__CHUNK,
                        input=True,
                        stream_callback=self.__callback)
        self.stream.start_stream()

        while self.stream.is_active():
            self.getBlockingFunction()


        self.stream.close()


    def getBlockingFunction(self):
        callback = self.queue.get()
        self.__handle_volume_data(callback)




# ----- just for testing purposes ----- #

def main():

    handler = soundHandler()

    def callback(volume):
        print("This is the volume: " + str(volume))

        return volume

    handler.start_stream(callback_function=callback)
    print("Do we get here")



if __name__ == "__main__":

    main()
