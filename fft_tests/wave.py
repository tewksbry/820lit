#Author: Samuel Resendez

import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import time

arr = []

def main():


    pa = pyaudio.PyAudio()


    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=44100,
                     input=True,
                     stream_callback=callback)
    stream.start_stream()

    while stream.is_active():
        time.sleep(20)
        stream.stop_stream()






def callback(in_data,frame_count,time_info,flag):
    global arr
    audio_data = np.fromstring(in_data, dtype= np.int16)

    fftData = abs(np.fft.rfft(audio_data)) ** 2

    which = fftData[1:].argmax() + 1

    if which != len(fftData) - 1:
        y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which + x1) * 44100 / 1024
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which * 44100 / 1024
        print "The freq is %f Hz." % (thefreq)


    return (in_data, pyaudio.paContinue)


if __name__ == "__main__":
    main()
