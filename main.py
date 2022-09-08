from instrument_utils.device_config import DeviceConfig
from calibration_file import Reflection

procedure_info = {
    "procedure_name": "get_info"
}

procedure_reset = {
    "procedure_name": "reset"
}

procedure_cfg_meas = {
    "procedure_name": "create_meas",
    "name_portA": 2,
    "name_portB": 2,
    "portA": 2,
    "portB": 2
}

procedure_set_width = {
    "procedure_name": "set_meas_width",
    "start_freq": 1e9,
    "stop_freq": 5e9,
    "points": 100
}

procedure_meas = {
    "procedure_name": "get_meas"
}

visa_device = DeviceConfig().create_device('n5245b')
print(visa_device.exec_procedure(**procedure_info))

visa_device.exec_procedure(**procedure_reset)
visa_device.exec_procedure(**procedure_cfg_meas)
visa_device.exec_procedure(**procedure_set_width)

data = visa_device.exec_procedure(**procedure_meas)
data = data.split(',')

re = data[0::2]
im = data[1::2]

content_list = []
df = (5e9 - 1e9) / (100 - 1)

for i in range(100):
    content = [1e9 + i * df, re[i], im[i]]
    content_list.append(content)

file_data = {
    "title": 2,
    "content": content_list
}

reflection_file = Reflection()
reflection_file.write(file_data)






