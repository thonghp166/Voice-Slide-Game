import librosa
import os.path as path
import hmmlearn.hmm as hmm
import numpy as np
import os
import pickle

# paths = ['down','left','right','up']
paths = ['left']
files = []
trained_files = []

def get_mfcc(filename):
    data, fs = librosa.load(filename, sr=None)
    mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
    return mfcc.T


def train(files, text):
    print('Trainning model '+ text)
    path = 'trained_model'
    all_mfcc = []
    for f in files[paths.index(text)]:
        all_mfcc.append(get_mfcc(f))
    model = hmm.GaussianHMM(n_components=30, n_iter=200, verbose=True)
    model.fit(X=np.vstack(all_mfcc), lengths=[
        mfcc.shape[0] for mfcc in all_mfcc])
    model_path = os.path.join(path, text + '.sav')
    pickle.dump(model, open(model_path, 'wb'))
    return model_path

def train_all():
    for path in paths:
        trained_files.append(train(files, path))

# r=root, d=directories, f = files
for path in paths:
    my_file = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.wav' in file:
                my_file.append(os.path.join(r, file))
    files.append(my_file)


print("Start training...")
train_all()
print("Done training. Models were saved in trained_model folder...")
