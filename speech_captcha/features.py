import numpy as np
from mfcc import MFCC
from scipy.io import wavfile
from scipy.signal import resample
from scipy.fftpack import dct

def calcDelta(feat, N):
	"""Compute delta features from a feature vector sequence.
    :param feat: A numpy array of size (NUMFRAMES by number of features) containing features. Each row holds 1 feature vector.
    :param N: For each frame, calculate delta features based on preceding and following N frames
    :returns: A numpy array of size (NUMFRAMES by number of features) containing delta features. Each row holds 1 delta feature vector.
    """
	if N < 1:
		raise ValueError('N must be an integer >= 1')
	NUMFRAMES = len(feat)
	denominator = 2 * sum([i**2 for i in range(1, N+1)])
	delta_feat = np.empty_like(feat)
	padded = np.pad(feat, ((N, N), (0, 0)), mode='edge')   # padded version of feat
	for t in range(NUMFRAMES):
		delta_feat[t] = np.dot(np.arange(-N, N+1), padded[t : t+2*N+1]) / denominator   # [t : t+2*N+1] == [(N+t)-N : (N+t)+N+1]
	return delta_feat

def extractFeatures(fname, delta=True, mfcc=False, scmc=False, scfc=False, norm=True):
    _,sig = wavfile.read(fname)
    sphinx_mfcc_class = MFCC(nfilt=40,
		    #ncep=20,
                    lowerf=100,
                    upperf=8000,
                    wlen=0.02)
    if mfcc:
     
        feats = sphinx_mfcc_class.sig2s2mfc(sig)
        
    if scmc or scfc:

        feats = sphinx_mfcc_class.sig2sc(sig, mag_feats=scmc)
        feats = np.log(feats)
        feats = dct(feats, n=40,norm='ortho')
    if norm:
        feat_mu = np.mean(feats, axis=0)
        feats -= feat_mu
    if delta:
        delta = calcDelta(feats,2)
        ddelta = calcDelta(delta,2)
        feats = np.concatenate((feats,delta), axis=1)
        feats = np.concatenate((feats,ddelta), axis=1)
    return feats