import pyvisa
import logging

from time import sleep
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
        # TODO: Добавить в процедуры возможность создать цикл
        # TODO: Добавить возможность провести математические операции,
        #   которые будут заданы в файле модели


        out = []
        cmd_list = self.procedure_list.get(kwargs.get("procedure_name"))

        for cmd_item in cmd_list:
            var = {}

            if "cmd" in cmd_item:
                cmd = cmd_item.get("cmd")
                if arg_list := cmd_item.get("args"):
                    args = []
                    for arg_name in arg_list:
                        arg = kwargs.get(arg_name)
                        args.append(arg)

                    if "{0}" in cmd:
                        tmp = self.send(cmd.format(*args))
                    else:
                        tmp = self.send(cmd % tuple(args))
                else:
                    tmp = self.send(cmd)

                if var_name := cmd_item.get("var"):
                    var.update({var_name: tmp})

                if math_command := cmd_item.get("math"):
                    tmp = self.__produce_result__(math_command, var)

                if tmp is not None:
                    out.append(tmp)
            else:
                n = 1
                tmp = None

                while cmd := cmd_item.get("cmd_%d" % n):
                    if arg_list := cmd_item.get("args_%d" % n):
                        args = []
                        for arg_name in arg_list:
                            if arg := kwargs.get(arg_name):
                                args.append(arg)

                        if "{0}" in cmd:
                            tmp = self.send(cmd.format(*args))
                        else:
                            tmp = self.send(cmd % tuple(args))
                    else:
                        tmp = self.send(cmd)

                    if var_name := cmd_item.get("var_%d" % n):
                        var.update({var_name: tmp})

                    n += 1

                if math_command := cmd_item.get("math"):
                    tmp = self.__produce_result__(math_command, var)

                if tmp is not None:
                    out.append(tmp)

        if len(out) == 1:
            return out[0]
        else:
            return out

    def __produce_result__(self, math_command, data):
        # TODO: Сделать более гибки обработчик математических комманд,
        #   или переделать его, потому что он не сможет обработать
        #   больше одной математической операции

        math_command = math_command.split(";")
        math_sequence = math_command[1].split(" ")

        a1 = data.get(math_sequence[0])
        a2 = data.get(math_sequence[2])

        match math_command[0]:
            case "complex":
                match math_sequence[1]:
                    case "+":
                        print("+")
                    case "-":
                        print("-")
                    case "*":
                        print("*")
                    case "/":
                        out = []

                        for i in range(0, len(a1), 2):
                            div = self.__complex_div__(a1[i], a1[i + 1], a2[i], a2[i + 1])
                            out.extend(div)
            case _:
                print("another")

        return out

    def __complex_div__(self, re_a, im_a, re_b, im_b):
        print(re_a)
        re_a = float(re_a)
        re_b = float(re_b)
        im_a = float(im_a)
        im_b = float(im_b)

        abs_2 = re_b ** 2 + im_b ** 2

        if abs_2 == 0:
            return [0, 0]
        else:
            re = (re_a * re_b + im_a * im_b) / abs_2
            im = (re_b * im_a + im_b * re_a) / abs_2

            return [re, im]


    def send(self, cmd):
        print("->", cmd)

        self.wait()
        if "?" in cmd:
            out = self.instrument.query(cmd)
            print("<-", out)

            self.instrument.write("*OPC")

            self.check_error()
            if "," in out:
                out = out.split(",")
                for i in range(len(out)):
                    out[i] = float(out[i])

            return out
        else:
            self.instrument.write(cmd)
            self.instrument.write("*OPC")

            if self.level == self.LEVEL_ERR or self.level == self.LEVEL_OPC_ERR:
                self.check_error()

    def check_error(self):
        err = self.instrument.query(":SYST:ERR?")

        if "No error" not in err:
            print("<-", err)

    def wait(self):
        opc = self.instrument.query("*OPC?")
        while opc != "+1" and opc != "1":
            sleep(0.01)
            opc = self.instrument.query("*OPC?")

    def disconnect(self):
        self.instrument.close()

