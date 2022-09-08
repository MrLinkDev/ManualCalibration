# Device - object, which contains some information
# about device and commands for configuring this device

class Device:
    vendor = None
    model = None
    port_num = None

    config = {}
    procedure_list = {}

    # TODO: add lists for commands
    def __init__(self, **kwargs):
        if vendor := kwargs.get("vendor"):
            self.vendor = vendor
        if model := kwargs.get("model"):
            self.model = model
        if port_num := kwargs.get("port_num"):
            self.port_num = port_num

        if address := kwargs.get("address"):
            self.config["address"] = address
        if timeout := kwargs.get("timeout"):
            self.config["timeout"] = timeout
        if termination := kwargs.get("termination"):
            self.config["termination"] = termination
        if log_level := kwargs.get("log_level"):
            self.config["log_level"] = log_level

        if procedure := kwargs.get("procedure"):
            self.procedure_list = procedure


