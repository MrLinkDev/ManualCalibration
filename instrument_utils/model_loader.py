import os
import json

from instrument_utils.visa_device import VisaDevice


class ModelLoader:
    DEFAULT_DIR = "instrument_model/"
    FILE_EXTENSION = ".model"

    device_list = {}

    def __init__(self, directory=DEFAULT_DIR):
        file_list = os.listdir(directory)
        for file in file_list:
            if not file.endswith(self.FILE_EXTENSION):
                file_list.remove(file)
            else:
                self.device_list[file.strip(self.FILE_EXTENSION)] = directory + file

    def create_device(self, model):
        device = VisaDevice(**model)
        return device

    def load_model(self, device_name=None, path=None):
        if device_name is not None:
            model_path = self.device_list.get(device_name)
        if path is not None:
            model_path = path

        data = json.load(open(model_path))

        model = {}
        if info := data.get("info"):
            model.update(info)
        if config := data.get("config"):
            model.update(config)
        if procedure := data.get("procedure"):
            model["procedure"] = procedure

        return model

    def get_device_list(self):
        return self.device_list.keys()











