from instrument_utils.device_model import DeviceModel
from raw_data_file import Reflection, Transition

procedure_info = {
    "procedure_name": "get_info"
}

procedure_reset = {
    "procedure_name": "reset"
}

procedure_cfg_meas_refl = {
    "procedure_name": "create_meas_reflection",
    "port": 1
}

procedure_cfg_meas_trans = {
    "procedure_name": "create_meas_transition",
    "port_a": 1,
    "port_b": 2
}

procedure_set_width = {
    "procedure_name": "set_meas_width",
    "start_freq": 1e9,
    "stop_freq": 5e9,
    "points": 100
}

procedure_refl_meas = {
    "procedure_name": "get_refl_meas"
}

procedure_trans_meas = {
    "procedure_name": "get_trans_meas"
}

visa_device = DeviceModel().create_device('n5245b')
print(visa_device.exec_procedure(**procedure_info))

visa_device.exec_procedure(**procedure_reset)
visa_device.exec_procedure(**procedure_cfg_meas_refl)
visa_device.exec_procedure(**procedure_set_width)

data = visa_device.exec_procedure(**procedure_refl_meas)

reflection_file = Reflection()
reflection_file.parse_data_to_file(data, port=1)
reflection_file.close()


visa_device.exec_procedure(**procedure_reset)
visa_device.exec_procedure(**procedure_cfg_meas_trans)
visa_device.exec_procedure(**procedure_set_width)

data = visa_device.exec_procedure(**procedure_trans_meas)

transition_file = Transition()
transition_file.parse_data_to_file(data, port_a=1, port_b=2)









