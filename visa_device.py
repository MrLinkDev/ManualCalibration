import pyvisa
import logging

from instrument_utils.device import Device


class VisaDevice(Device):
    LEVEL_NONE = 0
    LEVEL_ERR = 1
    LEVEL_OPC = 2
    LEVEL_OPC_ERR = 3

    instrument = None
    level = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__create_visa_device__(**self.config)

    def __create_visa_device__(self, **kwargs):
        if address := kwargs.get("address"):
            rm = pyvisa.ResourceManager()
            self.instrument = rm.open_resource(address)

            if timeout := kwargs.get("timeout"):
                self.instrument.timeout = timeout

            if termination := kwargs.get("termination"):
                self.instrument.read_termination = termination
                self.instrument.write_termination = termination

            if level := kwargs.get("level"):
                self.level = level
            else:
                self.level = self.LEVEL_NONE

    def exec_procedure(self, **kwargs):
        out = []
        cmd_list = self.procedure_list.get(kwargs.get("procedure_name"))

        for cmd_item in cmd_list:
            cmd = cmd_item.get("cmd")
            if arg_list := cmd_item.get("args"):
                args = []
                for arg_name in arg_list:
                    if arg := kwargs.get(arg_name):
                        args.append(arg)
                tmp = self.send(cmd % tuple(args))
            else:
                tmp = self.send(cmd)

            if tmp is not None:
                out.append(tmp)

        if len(out) == 1:
            return out[0]
        else:
            return out

    def send(self, cmd):
        if "?" in cmd:
            out = self.instrument.query(cmd)

            self.check_error()
            return out
        else:
            if self.level >= self.LEVEL_OPC:
                self.instrument.write("*OPC")

            self.instrument.write(cmd)

            if self.level >= self.LEVEL_OPC:
                self.instrument.write("*OPC?")

            if self.level == self.LEVEL_ERR or self.level == self.LEVEL_OPC_ERR:
                self.check_error()

    def check_error(self):
        err = self.instrument.query(":SYST:ERR?")

        if "No error" not in err:
            logging.error(err)
        else:
            logging.debug(err)

