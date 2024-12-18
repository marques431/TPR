import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
import argparse
import time
import joblib
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    parser.add_argument('-m', '--model',choices=['kmeans', 'dbscan'], nargs='?', required=True)
    args = parser.parse_args()

    # Read the Data
    input_file = "./ml_data/" + args.input
    dataset = pd.read_csv(input_file,sep=' ', low_memory=True, header=None, index_col=None)
    # print(dataset.head())
    # print(dataset.shape)
   
    features_min = dataset.min()
    features_max = dataset.max()
    dataset = (dataset - features_min) / (features_max - features_min)
    dataset = dataset.fillna(0)

    # Train the model
    print("Training the Model...")
    start_time = time.time()
    if args.model == 'kmeans':
        n_clusters = 3
        model = KMeans(n_clusters=n_clusters, random_state=0)
        model.fit(dataset)

        # Calculate the distances and the threshold
        distances = np.linalg.norm(dataset - model.cluster_centers_[model.labels_], axis=1)
        threshold = distances.mean() + 2 * distances.std()
    elif args.model == 'dbscan':
        model = DBSCAN(eps=0.3, min_samples=20)
        model.fit(dataset) 
        threshold = None

    else:
        return

    end_time = time.time()

    # Save the model
    model_file = "./models/" + args.model + ".pkl"
    joblib.dump({
        "model": model,
        "min": features_min,
        "max": features_max,
        "threshold": threshold
        }, model_file)

    
    print(f"Time taken to train the Model: {(end_time - start_time):.2f} seconds")
    print(f"Model saved in: {model_file}")
    print(f"Threshold defined: {threshold}")

     
if __name__ == '__main__':
    main()
