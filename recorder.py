import pyaudio
import math
import struct
import wave
import time
import os
import pygame
import pickle, librosa
import speech_recognition as sr_audio
import sounddevice as sd
import soundfile as sf

Threshold = 250

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 1

input_dir = r'/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/record'
move = ['down', 'up', 'right', 'left']
loaded_model = []

def load_model():
  for m in move:
    dir_file = "/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/train/trained_model/" + m + ".sav"
    loaded_model.append(pickle.load(open(dir_file, 'rb')))
  return loaded_model


def get_mfcc(filename):
  data, fs = librosa.load(filename, sr=None)
  mfcc = librosa.feature.mfcc(data, fs, hop_length=128, n_fft=1024)
  return mfcc.T


def transcribe_audio_sphinx(filename):
  r = sr_audio.Recognizer()
  with sr_audio.AudioFile(filename) as source:
    audio = r.record(source)
  text = r.recognize_google(audio)
  print('transcript: '+ text)
  return text

class Recorder:
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)
        return rms * 1000
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)
        self.load_model = load_model()
    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH
        for i in range(0, int(RATE / chunk * TIMEOUT_LENGTH)):
          data = self.stream.read(chunk)
          rec.append(data)
        while current <= end:
            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold:
                end = time.time() + TIMEOUT_LENGTH
            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))
    def write(self, recording):
        n_files = len(os.listdir(input_dir))
        filename = os.path.join(input_dir, '{}.wav'.format(n_files))
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Predicting')
        action = self.predict(filename)
        event = pygame.event.Event(pygame.USEREVENT, action=action)
        pygame.event.post(event)

    def predict(self, filename):
        results = [loaded_model[i].score(get_mfcc(filename)) for i in range(len(loaded_model))]
        print(results)
        maxi = max(results)
        if (maxi < -9000 and maxi > -12000):
          res = move[results.index(maxi)]
        else: res = 'No detected'
        print(res)
        return res

    def listen(self):
        input = self.stream.read(chunk)
        rms_val = self.rms(input)
        if rms_val > Threshold:
            print(rms_val)
            self.record()
