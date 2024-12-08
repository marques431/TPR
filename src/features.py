import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


def extratctSilenceActivity(data,threshold=0):
    if(data[0]<=threshold):
        s=[1]
        a=[]
    else:
        s=[]
        a=[1]
    for i in range(1,len(data)):
        if(data[i-1]>threshold and data[i]<=threshold):
            s.append(1)
        elif(data[i-1]<=threshold and data[i]>threshold):
            a.append(1)
        elif (data[i-1]<=threshold and data[i]<=threshold):
            s[-1]+=1
        else:
            a[-1]+=1
    return(s,a)

def ratios(data):
    up_down_packets = data[0] / data[2] if data[2] != 0 else 0
    down_up_packets = data[2] / data[0] if data[0] != 0 else 0
    up_down_bytes = data[1] / data[3] if data[3] != 0 else 0
    down_up_bytes = data[3] / data[1] if data[1] != 0 else 0
    
    return up_down_packets, down_up_packets, up_down_bytes, down_up_bytes

def extractStats(data):

    M1=np.mean(data,axis=0)
    Md1=np.median(data,axis=0)
    Std1=np.std(data,axis=0)
    
    silence,activity=extratctSilenceActivity(data)
    
    if len(silence)>0:
        silence_faux=np.array([len(silence),np.mean(silence),np.std(silence)])
    else:
        silence_faux=np.zeros(3)
        
    if len(activity)>0:
        activity_faux=np.array([len(activity),np.mean(activity),np.std(activity)])
    else:
        activity_faux=np.zeros(3)
    
    up_down_packets, down_up_packets, up_down_bytes, down_up_bytes = ratios(data)


    features=np.hstack((M1,Md1,Std1, silence_faux, activity_faux, up_down_packets, down_up_packets, up_down_bytes, down_up_bytes))
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
    parser.add_argument('-o', '--output', nargs='?', required=True)
    args = parser.parse_args()

    input_file = "./sampled_data/" + args.input
    data = np.loadtxt(input_file, dtype=int)

    filename = "./ml_data/" + args.output
    lenObsWindow = [5, 10, 30]
    slidingValue = 5

    features = extract_features(data, lenObsWindow, slidingValue)
    # print(features)
    np.savetxt(filename, features, fmt='%f')


if __name__ == '__main__':
    main()
