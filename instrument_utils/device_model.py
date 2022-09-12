import os
import json

from visa_device import VisaDevice


class DeviceModel:
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

    def create_device(self, device_name):
        model = self.__load_model__(self.device_list.get(device_name))

        device = VisaDevice(**model)
        return device

    def __load_model__(self, model_path):
        data = json.load(open(model_path))

        model = {}
        model.update(data.get("info"))
        model.update(data.get("config"))
        model["procedure"] = data.get("procedure")

        return model











