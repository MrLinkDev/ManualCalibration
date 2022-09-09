# Reflection file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ)\tS11(REAL)\tS11(IMAG)
# END
#
# Reflection file mask:
# FREQ(HZ)\tS%d%d(REAL)\tS%d%d(IMAG)


# Transition file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ)\tS11(REAL)\tS11(IMAG)\tS21(REAL)\tS21(IMAG)\tA2/A1(REAL)\tA2/A1(IMAG)\tS22(REAL)\tS22(IMAG)\tS12(REAL)\tS12(IMAG)\tA1/A2(REAL)\tA1/A2(IMAG)
# END
#
# Transition file mask:
# FREQ(HZ)\tS%d%d(REAL)\tS%d%d(IMAG)\tS%d%d(REAL)\tS%d%d(IMAG)\tA%d/A%d(REAL)\tA%d/A%d(IMAG)\tS%d%d(REAL)\tS%d%d(IMAG)\tS%d%d(REAL)\tS%d%d(IMAG)\tA%d/A%d(REAL)\tA%d/A%d(IMAG)


from os.path import exists
from os import remove


class CalibrationFile:
    DEFAULT_FILEPATH = "calibration/temp"
    file = None

    title_mask = None
    row_mask = None

    def __init__(self, path=DEFAULT_FILEPATH):
        if exists(path):
            remove(path)

        self.file = open(path, 'w')

    def write(self, data):
        self.file.write(self.title_mask.format(data.get("title")))
        self.file.write("\n")
        for d in data.get("content"):
            self.file.write(self.row_mask % tuple(d))
            self.file.write("\n")


class Reflection(CalibrationFile):
    title_mask = "FREQ(HZ)\tS{0}{0}(REAL)\tS{0}{0}(IMAG)"
    row_mask = "%s\t%s\t%s"

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


class Transition(CalibrationFile):
    title_mask = "FREQ(HZ)\tS{0}{0}(REAL)\tS{0}{0}(IMAG)\tS{1}{0}(REAL)\tS{1}{0}(IMAG)\ta{1}/a{0}(REAL)\ta{1}/a{0}(IMAG)\tS{1}{1}(REAL)\tS{1}{1}(IMAG)\tS{0}{1}(REAL)\tS{0}{1}(IMAG)\ta{0}/a{1}(REAL)\ta{0}/a{1}(IMAG)"
    row_mask = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s"

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

