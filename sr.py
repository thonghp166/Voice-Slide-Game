import speech_recognition as sr


voice = sr.AudioFile(
    '/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/train/left/left_0.wav')
r = sr.Recognizer()
with voice as source:
  audio = r.record(source)
r.recognize_google(audio)
