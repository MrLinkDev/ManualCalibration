import pyvisa
import logging


class VisaDevice:
    LEVEL_NONE = 0
    LEVEL_ERR = 1
    LEVEL_OPC = 2
    LEVEL_OPC_ERR = 3

    instrument = None
    level = None

    def __init__(self, **kwargs):
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
            logging.error("No address for instr")

    def get_info(self):
        out = self.instrument.query("*IDN?")
        return out

    def send(self, cmd):
        if "?" in cmd:
            logging.debug("[write]:\t%s", cmd)
            out = self.instrument.query(cmd)
            logging.debug("[read]:\t%s ")

            self.check_error()
            return out
        else:
            logging.debug("[write]:\t%s", cmd)

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

