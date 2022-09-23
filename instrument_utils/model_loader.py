import os
import json
import shutil

from instrument_utils.visa_device import VisaDevice


class ModelLoader:
    DEFAULT_DIR = "instrument_model/"
    FILE_EXTENSION = ".model"

    device_list = {}

    data_file = None
    data_dump = None

    def __init__(self, directory=DEFAULT_DIR):
        file_list = os.listdir(directory)
        for file in file_list:
            if not file.endswith(self.FILE_EXTENSION):
                file_list.remove(file)
            else:
                self.device_list[file.strip(self.FILE_EXTENSION)] = directory + file

    def create_device(self, model):
        return VisaDevice(**model)

    def load_model(self, device_name=None, path=None):
        model_path = None

        if device_name is not None:
            model_path = self.device_list.get(device_name)
        if path is not None:
            model_path = path

        self.data_file = open(model_path, 'r+')
        self.data_dump = json.load(self.data_file)

        model = {}

        if info := self.data_dump.get("info"):
            model.update(info)
        if config := self.data_dump.get("config"):
            model.update(config)
        if params := self.data_dump.get("params"):
            model["params"] = params
        if procedure := self.data_dump.get("procedure_dict"):
            model["procedure_dict"] = procedure

        return model

    def update_model(self, category, name, value):
        self.data_dump[category][name] = value

        self.data_file.seek(0)
        json.dump(self.data_dump, self.data_file, indent=4)
        self.data_file.truncate()

    def get_device_list(self):
        return self.device_list.keys()











