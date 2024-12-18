import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
import argparse
import time
import joblib
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances_argmin_min

# INFO: AAS Project Folder: /home/fabirino/Documents/Desktop/2023-24/1 Semestre/AAS/ProjetoAAS




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    parser.add_argument('-m', '--model', nargs='?', required=True)
    args = parser.parse_args()

    # Read the Data
    input_file = "./ml_data/" + args.input
    dataset = pd.read_csv(input_file,sep=' ', low_memory=True, header=None, index_col=None)
    # print(dataset.head())
    # print(dataset.shape)
    
    # Load the model
    model_file = "./models/" + args.model
    model_data = joblib.load(model_file)
    model = model_data["model"]
    features_min = model_data["min"]
    features_max = model_data["max"]
    threshold = model_data["threshold"]

    # Normalize the dataset with the same scale used in training
    dataset = (dataset - features_min) / (features_max - features_min)

    # Calculate the distances and classify
    print("Testing the model...")
    start_time = time.time()
    if isinstance(model, KMeans):
        # test_distances = np.min(
        #     [np.linalg.norm(dataset - center, axis=1) for center in model.cluster_centers_],
        #     axis=0
        #     )
        # pred_labels = np.where(test_distances > threshold, 0, 1)
        predict = model.predict(dataset)
        _, distances = pairwise_distances_argmin_min(dataset, model.cluster_centers_)
        anomalies = distances > threshold

        fig_file = "./figs/KMeans_" + args.input.split(".")[0] + ".png"
        plt.figure()
        plt.scatter(dataset.iloc[~anomalies, 0],dataset.iloc[~anomalies, 1], c="blue", label="Normal", alpha=0.7)
        plt.scatter(dataset.iloc[anomalies, 0], dataset.iloc[anomalies, 1], c="red", label="Anomalies", alpha=0.7)
        plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], c="black", s=100, label="Centroid", marker="X")
        plt.title("KMeans Anomaly Detection")
        plt.grid(True)
        plt.savefig(fig_file)

    elif isinstance(model, DBSCAN):
        predict = model.fit_predict(dataset)
        anomalies = predict == -1

        fig_file = "./figs/DBSCAN_" + args.input.split(".")[0] + ".png"
        plt.figure()
        plt.scatter(dataset.iloc[~anomalies, 0], dataset.iloc[~anomalies, 1], c="blue", label="Normal", alpha=0.7)
        plt.scatter(dataset.iloc[anomalies, 0], dataset.iloc[anomalies, 1], c="red", label="Anomalies", alpha=0.7)
        plt.title("DBSCAN Anomaly Detection")
        plt.grid(True)
        plt.savefig(fig_file)
        
    else:
        return


    end_time = time.time()

    # Print and save the results
    print(f"Time taken to test the Model: {(end_time - start_time):.2f} seconds")
    print("Results summary:")
    
    num_anomalies = np.sum(anomalies)
    total_points = len(dataset)
    anomaly_percentage = (num_anomalies / total_points) * 100
   
    print(f"Total number of samples: {total_points}")
    print(f"Number os anomalies detected: {num_anomalies}")
    print(f"Percentage of anomalies detected: {anomaly_percentage}")
    # unique, counts = np.unique(pred_labels, return_counts=True)
    # anomaly = 0
    # normal = 0
    # for label, count in zip(unique, counts):
    #     if label == 0:
    #         print(f"Class Anomaly: {count} instances")
    #         anomaly = count
    #     else:
    #         print(f"Class Normal: {count} instances")
    #         normal = count

    # print(f"% Anomaly Detected: {(anomaly / (anomaly+normal))*100:.2f} %")

    # Create and save the plot
    # pca = PCA(n_components=2)
    # reduced_data = pca.fit_transform(dataset)

    # plt.figure()
    # for i, label in enumerate(pred_labels):
    #     color = 'red' if label == 0 else 'blue'
    #     plt.scatter(reduced_data[i,0], reduced_data[i,1],c=color, s=10, alpha=0.7)

    # plt.title("Clusters: Normal (Blue) and Anomaly (Red)")
    # plt.grid(True)
    # plt.savefig(fig_file)
     
if __name__ == '__main__':
    main()
