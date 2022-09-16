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


class RawDataFile:
    DEFAULT_FILEPATH = "../calibration/"
    DEFAULT_FILE_EXTENSION = ".csv"

    file = None

    title_mask = None
    row_mask = None

    def __init__(self, path=DEFAULT_FILEPATH):
        self.file = open(path + self.DEFAULT_FILE_EXTENSION, 'w')

    def write(self, data):
        self.file.write(self.title_mask.format(*data.get("title")))
        self.file.write("\n")
        for d in data.get("content"):
            self.file.write(self.row_mask % tuple(d))
            self.file.write("\n")

    def close(self):
        self.file.close()

    def parse_data_to_file(self, data, **kwargs): ...


class Reflection(RawDataFile):
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

    def parse_data_to_file(self, data, **kwargs):
        freq_start = float(data[0])
        freq_stop = float(data[1])
        freq_step = float(data[2])
        points = int(data[3])

        data = data.pop(-1)
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


class Transition(RawDataFile):
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

    def parse_data_to_file(self, data, **kwargs):
        freq_start = float(data[0])
        freq_stop = float(data[1])
        freq_step = float(data[2])
        points = int(data[3])

        data = data[-6:]

        re = []
        im = []

        for i in range(len(data)):
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
