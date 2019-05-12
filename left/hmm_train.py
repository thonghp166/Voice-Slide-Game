#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'hmm'))
	print(os.getcwd())
except:
	pass

#%%
# mục tiêu: phân biệt lên và xuống
import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import librosa
import hmmlearn.hmm as hmm
from math import exp


#%%
def record_sound(filename, duration=1, fs=44100, play=False):
    sd.play( np.sin( 2*np.pi*940*np.arange(fs)/fs )  , samplerate=fs, blocking=True)
    sd.play( np.zeros( int(fs*0.2) ), samplerate=fs, blocking=True)
    data = sd.rec(frames=duration*fs, samplerate=fs, channels=1, blocking=True)
    if play:
        sd.play(data, samplerate=fs, blocking=True)
    sf.write(filename, data=data, samplerate=fs)

#record_sound('test.wav')


#%%
sd.play(data, samplerate=fs)
plt.figure(figsize=(15,5))
plt.plot(np.arange(fs*duration)/fs, data)


#%%
def record_data(prefix, n=25, duration=1):
    for i in range(n):
        print('{}_{}.wav'.format(prefix, i))
        record_sound('{}_{}.wav'.format(prefix, i), duration=duration)
        if i % 5 == 4:
            input("Press Enter to continue...")


#%%
record_data('len')


#%%
record_data('xuong')


#%%
def get_mfcc(filename):
    data, fs = librosa.load(filename, sr=None)
    mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
    return mfcc.T


#%%
n_sample = 25
data_len = [get_mfcc('len_{}.wav'.format(i)) for i in range(n_sample)]
data_xuong = [get_mfcc('xuong_{}.wav'.format(i)) for i in range(n_sample)]


#%%
model_len = hmm.GaussianHMM(n_components=30, verbose=True, n_iter=200)
model_len.fit(X=np.vstack(data_len), lengths=[x.shape[0] for x in data_len])


#%%
model_xuong = hmm.GaussianHMM(n_components=30, verbose=True, n_iter=200)
model_xuong.fit(X=np.vstack(data_xuong), lengths=[x.shape[0] for x in data_xuong])


#%%
mfcc = get_mfcc('xuong_0.wav')
model_len.score(mfcc), model_xuong.score(mfcc)


#%%
def get_prob(log_x1, log_x2):
    if log_x1 < log_x2:
        exp_x1_x2 = exp(log_x1-log_x2)
        return exp_x1_x2 / (1+exp_x1_x2), 1 / (1+exp_x1_x2)
    else:
        p = get_prob(log_x2, log_x1)
        return p[1], p[0]

for i in range(10):
    record_sound('test.wav')
    mfcc = get_mfcc('test.wav')
    log_plen, log_pxuong = model_len.score(mfcc), model_xuong.score(mfcc)
    plen, pxuong = get_prob(log_plen, log_pxuong)
    print(plen, pxuong, "len" if plen > pxuong else "xuong")


#%%
import speech_recognition as sr_audio

def transcribe_audio_sphinx(filename):
    r=sr_audio.Recognizer()
    with sr_audio.AudioFile(filename) as source:
        audio = r.record(source)
    text=r.recognize_sphinx(audio)
    print('transcript: '+text)
    return text

record_sound('hello.wav', duration=2)
transcribe_audio_sphinx('hello.wav')

#%% [markdown]
# This only waits for a user to press enter though, so you might want to use msvcrt ((Windows/DOS only) The msvcrt module gives you access to a number of functions in the Microsoft Visual C/C++ Runtime Library (MSVCRT)):
