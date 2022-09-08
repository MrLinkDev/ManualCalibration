import os
import json

from visa_device import VisaDevice


class DeviceConfig:
    DEFAULT_DIR = "instrument_config/"
    FILE_EXTENSION = ".cfg"

    device_list = {}

    def __init__(self, directory=DEFAULT_DIR):
        file_list = os.listdir(directory)
        for file in file_list:
            if not file.endswith(self.FILE_EXTENSION):
                file_list.remove(file)
            else:
                self.device_list[file.strip(self.FILE_EXTENSION)] = directory + file

    def create_device(self, device_name):
        config = self.__load_config__(self.device_list.get(device_name))

        device = VisaDevice(**config)
        return device

    def __load_config__(self, config_path):
        data = json.load(open(config_path))

        config = {}
        config.update(data.get("info"))
        config.update(data.get("config"))
        config["procedure"] = data.get("procedure")

        return config











