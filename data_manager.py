import os
import json

class DataManager:
    def __init__(self, filename="data.json"):
        self.filename = filename

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
        else:
            data = {}
        return data

    def save_data(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file)
