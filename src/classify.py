import argparse
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, f1_score, precision_score, recall_score
from sklearn.cluster import KMeans, DBSCAN
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model',choices=['kmeans', 'dbscan'], nargs='?', required=True)
    parser.add_argument('-n', '--normal_data', nargs='?', required=True)
    parser.add_argument('-a', '--anomalous_data', nargs='?', required=True)
    args = parser.parse_args()

    model_data = joblib.load(args.model)
    model = model_data["model"]

    normal_file = "./ml_data/" + args.normal_data
    anomalous_file = "./ml_data/" + args.anomalous_data

    normal = pd.read_csv(normal_file,sep=' ', low_memory=True, header=None, index_col=None)
    anomalous = pd.read_csv(anomalous_file, sep=' ', low_memory=True, header=None, index_col=None)

    # Normalize both datasets with the same min and max values from the normal dataset
    normal = (normal - model_data["min"]) / (model_data["max"] - model_data["min"])
    normal = normal.fillna(0)

    anomalous = (anomalous - model_data["min"]) / (model_data["max"] - model_data["min"])
    anomalous = anomalous.fillna(0)

    x_test = np.vstack([normal, anomalous])
    y_test = np.array([0] * len(normal) + [1] * len(anomalous))

    if isinstance(model, KMeans):
        y_pred = model.predict(x_test)
        y_pred = np.where(y_pred == 0, 0, 1)
    elif isinstance(model, DBSCAN):
        y_pred = model.fit_predict(x_test)
        y_pred = np.where(y_pred == -1, 1, 0)
    else:
        return

    cf_matrix = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cf_matrix, display_labels=["Normal", "Anomalous"])
    file_name = f"./results/{args.model}_{args.anomalous_data.split(".")[0]}_confusion_matrix.png"
    disp.plot(cmap=plt.cm.Blues)
    plt.savefig(file_name)

    print(f"Confusion Matrix saved in: {file_name}")
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    print(f"F1 Score: {f1:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")

    
if __name__ == "__main__":
    main()
