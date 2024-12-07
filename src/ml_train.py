import pandas as pd
from sklearn.metrics import classification_report
from sklearn.ensemble import  IsolationForest 
from sklearn.svm import OneClassSVM
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from mlxtend.evaluate import mcnemar_table
from mlxtend.evaluate import mcnemar
import seaborn as sns
import argparse
import time
import joblib
# INFO: AAS Project Folder: /home/fabirino/Documents/Desktop/2023-24/1 Semestre/AAS/ProjetoAAS




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    parser.add_argument('-o', '--output', nargs='?', required=False)
    args = parser.parse_args()

    # Read the Data
    input_file = "./ml_data/" + args.input
    dataset = pd.read_csv(input_file,sep=' ', low_memory=True, header=None, index_col=None)
    # print(dataset.head())
    # print(dataset.shape)
    
    # Normalize the data
    dataset = (dataset - dataset.min()) / (dataset.max() - dataset.min()) * 100
    dataset = dataset.fillna(0)
    # print(dataset)

    # Train the Model
    print('Training the Model...')
    start_time = time.time()  # Tempo inicial
    model = IsolationForest()
    model.fit(dataset)

    end_time = time.time()  # Tempo final 
    print(f"Time taken to train the Model: {(end_time - start_time):.2f} seconds")
    
    # TODO: Save the Model


if __name__ == '__main__':
    main()
