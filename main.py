import logging
import visa_instr
import ui


config = {
    "address": 'TCPIP0::192.168.110.128::inst0::INSTR',
    "timeout": 10000,
    "termination": "\n",
    "level": visa_instr.VisaInstrument.LEVEL_OPC_ERR
}


logging.basicConfig(format='[%(asctime)s] %(message)s')

instr = visa_instr.VisaInstrument(**config)
instr.get_info()

ui.main()

