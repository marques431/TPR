import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def extractStats(data):
    nSamp=data.shape
    print(data)

    M1=np.mean(data,axis=0)
    Md1=np.median(data,axis=0)
    Std1=np.std(data,axis=0)
    
    features=np.hstack((M1,Md1,Std1))
    return(features)

def extract_features(data, lenObsWindow, slidingValue):
    iobs = 0
    nSamples, nMetrics = data.shape
    while iobs*slidingValue < nSamples-max(lenObsWindow):
        obsFeatures = np.array([])
        for windowSize in lenObsWindow:
            for m in np.arange(nMetrics):
                wmFeatures = extractStats(data[iobs*slidingValue:iobs*slidingValue+windowSize,m])
                obsFeatures = np.hstack((obsFeatures, wmFeatures))
            iobs += 1
                
        if 'allFeatures' not in locals():
             allFeatures=obsFeatures.copy()
        else:
             allFeatures=np.vstack((allFeatures,obsFeatures))
    return(allFeatures)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    args = parser.parse_args()

    input_file = "./sampled_data/" + args.input
    lenObsWindow = [5, 10, 30]
    slidingValue = 5

    data = np.loadtxt(input_file, dtype=int)
    filename = "./ml_data/features.txt" # FIXME: mudar o nome do ficheiro

    features = extract_features(data, lenObsWindow, slidingValue)
    print(features)
    np.savetxt(filename, features, fmt='%d')


if __name__ == '__main__':
    main()
