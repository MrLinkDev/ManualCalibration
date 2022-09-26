# Reflection file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ),S11(REAL),S11(IMAG)
# END
#
# Reflection file mask:
# FREQ(HZ),S%d%d(REAL),S%d%d(IMAG)
import os.path


# Thru file structure:
#
# BEGIN CH1_DATA
# FREQ(HZ),S11(REAL),S11(IMAG),S21(REAL),S21(IMAG),A2/A1(REAL),A2/A1(IMAG),S22(REAL),S22(IMAG),S12(REAL),S12(IMAG),A1/A2(REAL),A1/A2(IMAG)
# END
#
# Thru file mask:
# FREQ(HZ),S%d%d(REAL),S%d%d(IMAG),S%d%d(REAL),S%d%d(IMAG),A%d/A%d(REAL),A%d/A%d(IMAG),S%d%d(REAL),S%d%d(IMAG),S%d%d(REAL),S%d%d(IMAG),A%d/A%d(REAL),A%d/A%d(IMAG)


class RawDataFile:
    DEFAULT_FOLDER = "calibration/"
    DEFAULT_FILE_EXTENSION = ".csv"

    file = None

    TITLE_MASK = None
    ROW_MASK = None

    def __init__(self, path=DEFAULT_FOLDER):
        print(path)
        if path == self.DEFAULT_FOLDER:
            path += "temp"

        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.file = open(path + self.DEFAULT_FILE_EXTENSION, 'w')

    def write(self, data):
        self.file.write(self.TITLE_MASK.format(*data.get("title")))
        self.file.write("\n")
        for d in data.get("content"):
            self.file.write(self.ROW_MASK % tuple(d))
            self.file.write("\n")

    def close(self):
        self.file.close()

    def parse_data_to_file(self, data, **kwargs): ...


class Reflection(RawDataFile):
    SHORT_FILENAME = "s%d"
    OPEN_FILENAME = "o%d"
    LOAD_FILENAME = "l%d"

    TITLE_MASK = "FREQ(HZ),S{0}{0}(REAL),S{0}{0}(IMAG)"
    ROW_MASK = "%s,%s,%s"

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

    def parse_data_to_file(self, data, **kwargs):
        freq_start = float(data[0])
        freq_stop = float(data[1])
        points = int(data[2])

        freq_step = (freq_stop - freq_start) / (points - 1)

        data = data.pop(-1)
        if type(data) is not list:
            data = data.split(',')

        re = data[0::2]
        im = data[1::2]

        content_list = []

        for i in range(points):
            content = [freq_start + i * freq_step, re[i], im[i]]
            content_list.append(content)

        file_data = {
            "title": str(kwargs.get("port")),
            "content": content_list
        }

        self.write(file_data)


class Thru(RawDataFile):
    CROSS_FILENAME = "t%d%d"

    TITLE_MASK = "FREQ(HZ),S{0}{0}(REAL),S{0}{0}(IMAG),S{1}{0}(REAL),S{1}{0}(IMAG),a{1}/a{0}(REAL),a{1}/a{0}(IMAG),S{1}{1}(REAL),S{1}{1}(IMAG),S{0}{1}(REAL),S{0}{1}(IMAG),a{0}/a{1}(REAL),a{0}/a{1}(IMAG)"
    ROW_MASK = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"

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

    def parse_data_to_file(self, data, **kwargs):
        freq_start = float(data[0])
        freq_stop = float(data[1])
        points = int(data[2])

        freq_step = (freq_stop - freq_start) / (points - 1)

        data = data[-6:]

        re = []
        im = []

        for i in range(len(data)):
            if type(data[i]) is not list:
                data[i] = data[i].split(',')

            re.append(data[i][0::2])
            im.append(data[i][1::2])

        content_list = []

        for i in range(points):
            content = [freq_start + i * freq_step,
                       re[0][i], im[0][i],
                       re[1][i], im[1][i],
                       re[2][i], im[2][i],
                       re[3][i], im[3][i],
                       re[4][i], im[4][i],
                       re[5][i], im[5][i]]
            content_list.append(content)

        file_data = {
            "title": [
                str(kwargs.get("port_a")),
                str(kwargs.get("port_b"))
            ],
            "content": content_list
        }

        self.write(file_data)

