import logging
import ui

from old_visa_device import VisaDevice
from instrument_utils.device_config import DeviceConfig


device_config = DeviceConfig()
device = device_config.create_device('n5245b')

visa_device = VisaDevice(**device.config)
print(visa_device.get_info())





