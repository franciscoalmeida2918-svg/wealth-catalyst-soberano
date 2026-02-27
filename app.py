# data_preprocessing.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(file_path):
    data = pd.read_csv(file_path)
    data = data.dropna()  # Remove missing values
    return data

def preprocess_data(data):
    X = data.drop('target', axis=1)
    y = data['target']
    X = StandardScaler().fit_transform(X)  # Feature scaling
    return X, y

def split_data(X, y, test_size=0.2):
    return train_test_split(X, y, test_size=test_size, random_state=42)
