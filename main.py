from instrument_utils.device_config import DeviceConfig

procedure_info = {
    "procedure_name": "get_info"
}

procedure_meas = {
    "procedure_name": "create_meas",
    "name_portA": 1,
    "name_portB": 2,
    "portA": 1,
    "portB": 2
}

procedure_set_width = {
    "procedure_name": "set_meas_width",
    "start_freq": 1e9,
    "stop_freq": 5e9,
    "points": 100
}

visa_device = DeviceConfig().create_device('n5245b')
print(visa_device.exec_procedure(**procedure_info))

visa_device.exec_procedure(**procedure_meas)
visa_device.exec_procedure(**procedure_set_width)




