import json
import numpy as np

class HousePredictor:

    def __init__(self):

        with open("model/model.json") as f:
            model = json.load(f)

        with open("model/scaler.json") as f:
            scaler = json.load(f)

        self.weights = np.array(
            model["weights"]
        )

        self.bias = model["bias"]

        self.mean = scaler["mean"]
        self.std = scaler["std"]

    def predict(self,
                rm,
                lstat,
                ptratio):

        rm = (
            rm - self.mean["RM"]
        ) / self.std["RM"]

        lstat = (
            lstat - self.mean["LSTAT"]
        ) / self.std["LSTAT"]

        ptratio = (
            ptratio - self.mean["PTRATIO"]
        ) / self.std["PTRATIO"]

        x = np.array([
            rm,
            lstat,
            ptratio
        ])

        prediction = (
            np.dot(x, self.weights)
            + self.bias
        )

        return prediction