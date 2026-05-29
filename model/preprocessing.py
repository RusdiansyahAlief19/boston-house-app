import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def perform_class_conditional_imputation(df, target_col, feature_cols, num_classes=5):
    df_clean = df.copy()
    df_clean['class_group'] = pd.qcut(df_clean[target_col], q=num_classes, labels=False)
    for col in feature_cols:
        if df_clean[col].isnull().any():
            class_means = df_clean.groupby('class_group')[col].transform('mean')
            df_clean[col] = df_clean[col].fillna(class_means)
    df_clean = df_clean.drop(columns=['class_group'])
    return df_clean

def calculate_zscore_params(df_train, feature_cols):
    params = {}
    for col in feature_cols:
        mean = df_train[col].mean()
        std = df_train[col].std()
        params[col] = {'mean': mean, 'std': std}
    return params

def apply_zscore_normalization(df, feature_cols, params):
    df_norm = df.copy()
    for col in feature_cols:
        mean = params[col]['mean']
        std = params[col]['std']
        df_norm[col] = (df_norm[col] - mean) / std
    return df_norm

def split_dataset(df, test_size=0.2, random_state=42):
    return train_test_split(df, test_size=test_size, random_state=random_state)
