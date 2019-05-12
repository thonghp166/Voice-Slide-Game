import librosa
import os.path as path
import os
import pickle

paths = ['down','left','right','up']

files = []
# r=root, d=directories, f = files
for path in paths:
  for r, d, f in os.walk(path):
      for file in f:
          if '.wav' in file:
              files.append(os.path.join(r, file))

for f in files:
    print(f)
