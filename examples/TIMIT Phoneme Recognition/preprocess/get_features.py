__author__ = 'joerg'

# http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/


import numpy as np
from scikits.audiolab import Sndfile, play
import speech_features.features as sf




def get_features(filename, numcep, numfilt, winlen, winstep, grad):

    f = Sndfile(filename, 'r')

    frames = f.nframes
    samplerate = f.samplerate
    data = f.read_frames(frames)
    data = np.asarray(data)

    #numcep=12 #18
    #numfilt = 26 #40
    #winlen=0.025,winstep=0.01

    #calc mfcc
    feat_raw,energy = sf.fbank(data, samplerate,winlen,winstep, nfilt=numfilt)
    feat = np.log(feat_raw)
    feat = sf.dct(feat, type=2, axis=1, norm='ortho')[:,:numcep]
    feat = sf.lifter(feat,L=22)
    feat = np.asarray(feat)

    #calc log energy
    log_energy = np.log(energy) #np.log( np.sum(feat_raw**2, axis=1) )
    log_energy = log_energy.reshape([log_energy.shape[0],1])

    #concatenate mfcc and log energy
    mat = np.concatenate((feat,log_energy),axis=1)

    #calc first order derivatives
    if grad >= 1:
        gradf = np.gradient(mat)[0]

    #calc second order derivatives
    if grad == 2:
        grad2f = np.gradient(gradf)[0]

    #concatenate
    if grad == 1:
        finfa = np.concatenate((mat,gradf),axis=1)
    elif grad == 2:
        finfa = np.concatenate((mat,gradf, grad2f),axis=1)
    else:
        finfa = mat

    #normilize signals
    finfa = ( finfa - np.mean(finfa, axis=0) ) / np.std(finfa, axis=0)

    return finfa, frames, samplerate





