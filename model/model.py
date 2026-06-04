import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import json

df = pd.read_csv("https://raw.githubusercontent.com/RusdiansyahAlief19/boston-house-app/refs/heads/main/data/housing.csv")

X = df[['RM', 'LSTAT', 'PTRATIO']]
y = df['MEDV']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

mean = X_train.mean()
std = X_train.std()

print("===== Mean & Std ====")
print(mean)
print(std)
print("======================\n")

def zscore_norm (df, mean, std):
    return (df - mean) / std

X_train = zscore_norm(X_train, mean, std)
X_test = zscore_norm(X_test, mean, std)

class RegresiLinearBerganda:

    def __init__(self,
                 learning_rate=0.01,
                 iterations=1000):

        self.lr = learning_rate
        self.iterations = iterations

    def fit(self, X, y):

        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        self.loss_history = []

        for _ in range(self.iterations):

            y_pred = np.dot(X, self.weights) + self.bias

            dw = (1/n_samples) * np.dot(
                X.T,
                (y_pred - y)
            )

            db = (1/n_samples) * np.sum(
                y_pred - y
            )

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            mse = np.mean(
                (y - y_pred) ** 2
            )

            self.loss_history.append(mse)

    def predict(self, X):

        return np.dot(X, self.weights) + self.bias

model = RegresiLinearBerganda()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)

    return 1 - (ss_res / ss_tot)

print("===== RMSE & r^2 =====")
print("RMSE =", rmse(y_test, y_pred))
print("R²   =", r2_score(y_test, y_pred))
print("======================")

model_data = {
    "weights" : model.weights.tolist(),
    "bias" : model.bias
}

with open("model/model.json", "w") as f:
    json.dump(model_data, f, indent=4)

scaler_data = {
    "mean": mean.to_dict(),
    "std": std.to_dict()
}

with open("model/scaler.json", "w") as f:
    json.dump(scaler_data, f, indent=4)