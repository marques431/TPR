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
import argparse
import time
import joblib
import numpy as np

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
    kmeans = model_data["kmeans"]
    features_min = model_data["min"]
    features_max = model_data["max"]
    threshold = model_data["threshold"]

    # Normalize the dataset with the same scale used in training
    start_time = time.time()
    dataset = (dataset - features_min) / (features_max - features_min)

    # Calculate the distances and classify
    test_distances = np.min(
            [np.linalg.norm(dataset - center, axis=1) for center in kmeans.cluster_centers_],
            axis=0
            )
    pred_labels = np.where(test_distances > threshold, 0, 1)
    end_time = time.time()

    # Print and save the results
    print(f"\nPredictions done. Distances calculated with a threshold equal to: {threshold}")
    print(f"Time taken to test the Model: {(end_time - start_time):.2f} seconds")
    print("Results summary:")
    unique, counts = np.unique(pred_labels, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"Class {label}: {count} instances")

    fig_file = "./figs/" + args.input.split(".")[0] + ".png"


    print(f"Plot saved in: {fig_file}")
     
if __name__ == '__main__':
    main()
