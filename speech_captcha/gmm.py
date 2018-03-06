import os
import numpy as np
from sklearn import mixture
import pickle
import sys
from captcha import settings
from sklearn.externals import joblib
from captcha import settings

def loadGMM(gmmFile):
	gmm = joblib.load(gmmFile)
	return gmm

def test(data_f, ncomps, gmmFileDir):
	gmm_P = loadGMM(gmmFileDir+"/P/"+str(ncomps)+"/sklearnGMM.pkl")
	gmm_N = loadGMM(gmmFileDir+"/N/"+str(ncomps)+"/sklearnGMM.pkl")
	
		
	ll_P = sum(gmm_P.score_samples(data_f))
	ll_N = sum(gmm_N.score_samples(data_f))
	
	score = ll_P - ll_N
	label = int(score > settings.FORGERY_THRESH)
	return label

if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit()
    if len(sys.argv) == 6:
    	print "HELLO"
        testFiles(sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        print "arg1 - in file list, arg2 - nComp, arg3 - output file, argv4-actaul label, argv5-gmm output Folder"
        sys.exit()

# testFiles('../files/folds/BR/BR_p.fold0', '../GMMs/BR/fold_0/', 1, "test_result.txt")
