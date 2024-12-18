import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import GridSearchCV
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.metrics import classification_report
# from sklearn.ensemble import GradientBoostingClassifier, IsolationForest, RandomForestClassifier
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# import matplotlib.pyplot as plt
# from mlxtend.evaluate import mcnemar_table
# from mlxtend.evaluate import mcnemar
# import seaborn as sns
from sklearn.cluster import KMeans
import argparse
import time
import joblib
import numpy as np

# INFO: AAS Project Folder: /home/fabirino/Documents/Desktop/2023-24/1 Semestre/AAS/ProjetoAAS




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    parser.add_argument('-o', '--output', nargs='?', required=True)
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
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(dataset)

    # Calculate the distances and the threshold
    distances = np.linalg.norm(dataset - kmeans.cluster_centers_[kmeans.labels_], axis=1)
    threshold = distances.mean() + 2 * distances.std()
    end_time = time.time()

    # Save the model
    model_file = "./models/" + args.output
    joblib.dump({
        "kmeans": kmeans,
        "min": features_min,
        "max": features_max,
        "threshold": threshold
        }, model_file)

    
    print(f"Time taken to train the Model: {(end_time - start_time):.2f} seconds")
    print(f"Model saved in: {model_file}")
    print(f"Threshold defined: {threshold}")

     
if __name__ == '__main__':
    main()
