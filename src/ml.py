import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from mlxtend.evaluate import mcnemar_table
from mlxtend.evaluate import mcnemar
import seaborn as sns

# INFO: AAS Project Folder: /home/fabirino/Documents/Desktop/2023-24/1 Semestre/AAS/ProjetoAAS

