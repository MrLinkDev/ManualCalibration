# Reflection file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ);S11(REAL);S11(IMAG)
# END
#
# Reflection file mask:
# FREQ(HZ);S%d%d(REAL);S%d%d(IMAG)


# Transition file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ);S11(REAL);S11(IMAG);S21(REAL);S21(IMAG);A2/A1(REAL);A2/A1(IMAG);S22(REAL);S22(IMAG);S12(REAL);S12(IMAG);A1/A2(REAL);A1/A2(IMAG)
# END
#
# Transition file mask:
# FREQ(HZ);S%d%d(REAL);S%d%d(IMAG);S%d%d(REAL);S%d%d(IMAG);A%d/A%d(REAL);A%d/A%d(IMAG);S%d%d(REAL);S%d%d(IMAG);S%d%d(REAL);S%d%d(IMAG);A%d/A%d(REAL);A%d/A%d(IMAG)


from os.path import exists
from os import remove


class CalibrationFile:
    DEFAULT_FILEPATH = "calibration/temp"
    file = None

    def __init__(self, path=DEFAULT_FILEPATH):
        if exists(path):
            remove(path)

        self.file = open(path, 'w')


class Reflection(CalibrationFile):
    title_mask = "FREQ(HZ);S{0}{0}(REAL);S{0}{0}(IMAG)"
    row_mask = "%s;%s;%s"

    # Input data format:
    # data = {
    #   "title": port,
    #   "content": [
    #       line_1,
    #       line_2,
    #       ...,
    #       line_n
    #   ]
    # }
    def write(self, data):
        self.file.write("BEGIN\n")
        self.file.write(self.title_mask.format(data.get("title")))
        self.file.write("\n")
        for d in data.get("content"):
            self.file.write(self.row_mask % tuple(d))
            self.file.write("\n")
        self.file.write("END\n")


class Transmission(CalibrationFile):
    title_mask = "FREQ(HZ);S{0}{0}(REAL);S{0}{0}(IMAG);S{1}{0}(REAL);S{1}{0}(IMAG);a{1}/a{0}(REAL);a{1}/a{0}(IMAG);S{1}{1}(REAL);S{1}{1}(IMAG);S{0}{1}(REAL);S{0}{1}(IMAG);a{0}/a{1}(REAL);a{0}/a{1}(IMAG)"
    row_mask = "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s"

    # Input data format:
    # data = {
    #   "title": [
    #       port_a,
    #       port_b
    #   ],
    #   "content": [
    #       line_1,
    #       line_2,
    #       ...,
    #       line_n
    #   ]
    # }
    def write(self, data):
        self.file.write("BEGIN\n")
        self.file.write(self.title_mask.format(data.get("title")))
        self.file.write("\n")
        for d in data.get("content"):
            self.file.write(self.row_mask % tuple(d))
            self.file.write("\n")
        self.file.write("END\n")