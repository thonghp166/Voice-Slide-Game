import sounddevice as sd
import soundfile as sf
import numpy as np


def record_sound(filename, duration=1, fs=44100, play=False):
    sd.play(np.sin(2*np.pi*500*np.arange(fs)/fs), samplerate=fs, blocking=True)
    sd.play(np.zeros(int(fs*0.2)), samplerate=fs, blocking=True)
    data = sd.rec(frames=duration*fs, samplerate=fs, channels=1, blocking=True)
    if play:
        sd.play(data, samplerate=fs, blocking=True)
    sf.write(filename, data=data, samplerate=fs)


def record_data(prefix, n=25, duration=1):
    for i in range(n):
        print('{}_{}.wav'.format(prefix, i))
        record_sound('{}_{}.wav'.format(prefix, i), duration=duration)
        if i % 5 == 4:
            input("Press Enter to continue...")
