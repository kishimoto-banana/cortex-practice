import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pickle

labels = ["setosa", "versicolor", "virginica"]


class PythonPredictor:
    def __init__(self, config):
        if os.environ.get("AWS_ACCESS_KEY_ID"):
            s3 = boto3.client("s3")
        else:
            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        s3.download_file(config["bucket"], config["key"], "/tmp/another-model.pkl")
        self.model = pickle.load(open("/tmp/another-model.pkl", "rb"))

    def predict(self, payload):
        measurements = [
            payload["sepal_length"],
            payload["sepal_width"],
            payload["petal_length"],
            payload["petal_width"],
        ]
        label_id = self.model.predict([measurements])[0]
        return labels[label_id]
