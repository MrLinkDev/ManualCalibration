import tkinter as tk

from tkinter import ttk
from tkinter import filedialog as fd
from instrument_utils.model_loader import ModelLoader, VisaDevice
from utils.procedure_dict import *


class App:
    model_loader = None
    device_model = None
    visa_device = None

    root = None

    model_label = None
    model_frame = None
    device_frame = None
    params_frame = None
    cal_frame = None
    model = None

    device_list = None
    load_label = None
    filepath_box = None
    filepicker_button = None
    filename = None

    info_label = None
    address_box = None
    connect_button = None

    start_freq_label = None
    stop_freq_label = None
    points_label = None
    rbw_label = None
    power_label = None

    start_freq_sb = None
    stop_freq_sb = None
    points_sb = None
    rbw_sb = None
    power_sb = None

    start_freq_units = None
    stop_freq_units = None
    rbw_units = None
    power_units = None

    config_button = None

    freq_units_list = ["Гц", "кГц", "МГц", "ГГц"]

    cal_labels = []
    port_labels = []

    cal_buttons = []

    def __init__(self):
        self.model_loader = ModelLoader()

        root = tk.Tk()

        root.geometry("730x480")
        root.title("Raw data catcher")
        root.resizable(False, False)

        self.__configure_ui__(root)
        self.root = root

    def show(self):
        self.root.mainloop()

    def __configure_ui__(self, root):
        self.model_frame = ttk.Frame(root, relief="groove")
        self.device_frame = ttk.Frame(root, relief="groove")
        self.params_frame = ttk.Frame(root, relief="groove")
        self.cal_frame = ttk.Frame(root, relief="groove")

        self.model_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nwes")
        self.device_frame.grid(row=1, column=0, padx=10, sticky="nwes")
        self.params_frame.grid(row=2, rowspan=2, column=0, padx=10, pady=10, sticky="nwes")
        self.cal_frame.grid(row=0, rowspan=3, column=1, padx=10, pady=10, sticky="nwes")

        self.__configure_model_frame__(self.model_frame)
        self.__configure_device_frame__(self.device_frame)
        self.__configure_params_frame__(self.params_frame)
        self.__configure_cal_frame__(self.cal_frame)

    def __configure_model_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=1)

        self.model_label = ttk.Label(frame, text="Выбор модели:")
        self.model_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        device_list = ["Загрузить модель..."]
        device_list.extend(self.model_loader.get_device_list())

        self.model = tk.StringVar()
        self.device_list = ttk.Combobox(frame, values=device_list)
        self.device_list.current(0)
        self.device_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5)
        self.device_list.bind("<<ComboboxSelected>>", self.__combobox_callback__)

        frame.grid_rowconfigure(2, weight=1, minsize=20)

        self.load_label = ttk.Label(frame, text="Загрузка из файла:")
        self.load_label.grid(row=3, column=0, columnspan=1, sticky="sw", padx=5)

        self.filepath_box = ttk.Entry(frame)
        self.filepath_box.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.filepicker_button = ttk.Button(frame, text="Выбрать", command=lambda: self.__pick_file__())
        self.filepicker_button.grid(row=4, column=2, padx=5, pady=5)

    def __configure_device_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=1)

        self.info_label = ttk.Label(frame, text="Прибор:")
        self.info_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.address_box = ttk.Entry(frame)
        self.address_box.grid(row=1, column=0, columnspan=3, sticky="we", padx=5)

        self.connect_button = ttk.Button(frame, text="Подключиться", command=lambda: self.__create_visa_device__())
        self.connect_button.grid(row=2, column=2, columnspan=1, padx=5, pady=5, sticky="nsew")

    def __configure_params_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=1)

        self.start_freq_label = ttk.Label(frame, text="Начальная\nчастота:")
        self.start_freq_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.stop_freq_label = ttk.Label(frame, text="Конечная\nчастота:")
        self.stop_freq_label.grid(row=1, column=0, sticky="w", padx=5)

        self.points_label = ttk.Label(frame, text="Количество\nточек:")
        self.points_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.rbw_label = ttk.Label(frame, text="RBW:")
        self.rbw_label.grid(row=3, column=0, sticky="w", padx=5)

        self.power_label = ttk.Label(frame, text="Мощность:")
        self.power_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.start_freq_sb = ttk.Spinbox(frame, from_=0, to=1000000000000)
        self.start_freq_sb.grid(row=0, column=1, sticky="ew")

        self.stop_freq_sb = ttk.Spinbox(frame, from_=0, to=1000000000000)
        self.stop_freq_sb.grid(row=1, column=1, sticky="ew")

        self.points_sb = ttk.Spinbox(frame, from_=0, to=1000000)
        self.points_sb.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)

        self.rbw_sb = ttk.Spinbox(frame, from_=0, to=1000000000000)
        self.rbw_sb.grid(row=3, column=1, sticky="ew")

        self.power_sb = ttk.Spinbox(frame, from_=-1000, to=1000)
        self.power_sb.grid(row=4, column=1, sticky="ew")

        self.start_freq_units = ttk.Combobox(frame, values=self.freq_units_list, width=6)
        self.start_freq_units.current(0)
        self.start_freq_units.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        self.stop_freq_units = ttk.Combobox(frame, values=self.freq_units_list, width=6)
        self.stop_freq_units.current(0)
        self.stop_freq_units.grid(row=1, column=2, sticky="e", padx=5, pady=5)

        self.rbw_units = ttk.Combobox(frame, values=self.freq_units_list, width=6)
        self.rbw_units.current(0)
        self.rbw_units.grid(row=3, column=2, sticky="e", padx=5, pady=5)

        self.power_units = ttk.Label(frame, text="дБм")
        self.power_units.grid(row=4, column=2, sticky="w", padx=5, pady=5)

        frame.grid_rowconfigure(5, weight=1, minsize=20)

        self.config_button = ttk.Button(frame, text="Загрузить настройки", command=lambda: self.__config_button_callback__())
        self.config_button.grid(row=6, column=1, columnspan=2, sticky="e", padx=5, pady=5)

        self.start_freq_label.config(state="disabled")
        self.stop_freq_label.config(state="disabled")
        self.points_label.config(state="disabled")
        self.rbw_label.config(state="disabled")
        self.power_label.config(state="disabled")
        self.start_freq_sb.config(state="disabled")
        self.stop_freq_sb.config(state="disabled")
        self.points_sb.config(state="disabled")
        self.rbw_sb.config(state="disabled")
        self.power_sb.config(state="disabled")
        self.start_freq_units.config(state="disabled")
        self.stop_freq_units.config(state="disabled")
        self.rbw_units.config(state="disabled")
        self.power_units.config(state="disabled")
        self.config_button.config(state="disabled")

    def __configure_cal_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        for i in range(9):
            for j in range(5):
                if i == 0:
                    t = ""
                    if j == 1:
                        t = "КЗ"
                    if j == 2:
                        t = "ХХ"
                    if j == 3:
                        t = "НАГРУЗКА"
                    if j == 4:
                        t = "ПЕРЕДАЧА\n(из порта 1)"

                    if j != 0:
                        self.cal_labels.append(ttk.Label(frame, text=t))
                        self.cal_labels[j-1].grid(row=i, column=j, padx=5, pady=5, sticky="ns")
                else:
                    if j == 0:
                        port_name = "ПОРТ %d" % i
                        self.port_labels.append(ttk.Label(frame, text=port_name))
                        self.port_labels[i-1].grid(row=i, column=j, padx=5, pady=5, sticky="we")
                    else:
                        if (i - 1) * 4 + (j - 1) == 3:
                            self.cal_buttons.append(None)
                            continue
                        self.cal_buttons.append(
                            tk.Button(
                                frame,
                                text=("Калибровка\n[❌]"),
                                justify="center",
                                command=lambda p=i, d=j: self.__cal_button_callback__(p, d)
                            )
                        )
                        self.cal_buttons[(i - 1) * 4 + (j - 1)].grid(row=i, column=j, padx=5, pady=5)
                        self.cal_buttons[(i - 1) * 4 + (j - 1)].config(state="disabled")


    def __pick_file__(self):
        filetype = (
            ("Device model file", "*.model"),
            ("All files", "*.*"))

        self.filename = fd.askopenfile(
            title="Open model file",
            initialdir="instrument_model",
            filetypes=filetype).name

        self.filepath_box.delete(0, tk.END)
        self.filepath_box.insert(0, self.filename)
        self.filepath_box.xview("end")

        self.device_model = self.model_loader.load_model(path=self.filename)

        self.__fill_info__(self.device_model)

    def __combobox_callback__(self, obj):
        model = self.device_list.get()
        if model != "Загрузить модель...":
            self.load_label.config(state="disabled")
            self.filepath_box.config(state="disabled")
            self.filepicker_button.config(state="disabled")

            self.device_model = self.model_loader.load_model(device_name=model)

            self.__fill_info__(self.device_model)
        else:
            self.load_label.config(state="enabled")
            self.filepath_box.config(state="enabled")
            self.filepicker_button.config(state="enabled")

            if self.filepath_box.get() == "":
                self.info_label.config(text="Прибор: ")
                self.address_box.delete(0, tk.END)
            else:
                self.device_model = self.model_loader.load_model(path=self.filepath_box.get())
                self.__fill_info__(self.device_model)

    def __fill_info__(self, model):
        if info := model.get("vendor") + ", " + model.get("model"):
            self.info_label.config(text="Прибор: " + info)
        else:
            self.info_label.config(text="Прибор: Unknown")

        if address := model.get("address"):
            self.address_box.delete(0, tk.END)
            self.address_box.insert(0, address)
        else:
            self.address_box.delete(0, tk.END)

    def __create_visa_device__(self):
        address = self.address_box.get()
        if self.device_model.get("address") != address:
            self.device_model["address"] = address

        self.visa_device = VisaDevice(**self.device_model)

        # TODO: Добавить проверку производителя и модели.
        #   Если не совпадают, то найти файл с тем же названием,
        #   что и модель прибора. Если такого файла нет, то проверить
        #   производителя. Если производитель совпал, то показать
        #   предупреждение о возможной несовместимости команд

        if self.visa_device is not None:
            self.model_label.config(state="disabled")
            self.device_list.config(state="disabled")
            self.load_label.config(state="disabled")
            self.filepath_box.config(state="disabled")
            self.filepicker_button.config(state="disabled")

            self.address_box.config(state="disabled")
            self.connect_button.config(text="Отключить", command=lambda: self.__destroy_visa_device__())

            self.start_freq_label.config(state="enabled")
            self.stop_freq_label.config(state="enabled")
            self.points_label.config(state="enabled")
            self.rbw_label.config(state="enabled")
            self.power_label.config(state="enabled")
            self.start_freq_sb.config(state="enabled")
            self.stop_freq_sb.config(state="enabled")
            self.points_sb.config(state="enabled")
            self.rbw_sb.config(state="enabled")
            self.power_sb.config(state="enabled")
            self.start_freq_units.config(state="enabled")
            self.stop_freq_units.config(state="enabled")
            self.rbw_units.config(state="enabled")
            self.power_units.config(state="enabled")
            self.config_button.config(state="normal")

            if params := self.device_model.get("params"):
                if start_freq := params.get("start_freq"):
                    self.start_freq_sb.set(start_freq)
                if stop_freq := params.get("stop_freq"):
                    self.stop_freq_sb.set(stop_freq)
                if points := params.get("points"):
                    self.points_sb.set(points)
                if rbw := params.get("rbw"):
                    self.rbw_sb.set(rbw)
                if power := params.get("power"):
                    self.power_sb.set(power)

            if port_num := self.device_model.get("port_num"):
                for i in range(port_num):
                    for j in range(4):
                        if (i * 4 + j) == 3:
                            continue

                        self.cal_buttons[i * 4 + j].config(state="normal")

    def __destroy_visa_device__(self):
        self.visa_device.disconnect()
        self.visa_device = None

        self.model_label.config(state="enabled")
        self.device_list.config(state="enabled")

        if self.device_list.get() == "Загрузить модель...":
            self.load_label.config(state="enabled")
            self.filepath_box.config(state="enabled")
            self.filepicker_button.config(state="enabled")

        self.address_box.config(state="enabled")
        self.connect_button.config(text="Подключить", command=lambda: self.__create_visa_device__())

        self.start_freq_label.config(state="disabled")
        self.stop_freq_label.config(state="disabled")
        self.points_label.config(state="disabled")
        self.rbw_label.config(state="disabled")
        self.power_label.config(state="disabled")
        self.start_freq_sb.config(state="disabled")
        self.stop_freq_sb.config(state="disabled")
        self.points_sb.config(state="disabled")
        self.rbw_sb.config(state="disabled")
        self.power_sb.config(state="disabled")
        self.start_freq_units.config(state="disabled")
        self.stop_freq_units.config(state="disabled")
        self.rbw_units.config(state="disabled")
        self.power_units.config(state="disabled")
        self.config_button.config(state="disabled")

        if port_num := self.device_model.get("port_num"):
            for i in range(port_num):
                for j in range(4):
                    if (i * 4 + j) == 3:
                        continue

                    self.cal_buttons[i * 4 + j].config(state="disabled")

    def __cal_button_callback__(self, port, cal_type):
        if "❌" in self.cal_buttons[(port - 1) * 4 + (cal_type - 1)].cget('text'):
            self.cal_buttons[(port - 1) * 4 + (cal_type - 1)].config(text="Калибровка\n[✔]")
        elif "✔" in self.cal_buttons[(port - 1) * 4 + (cal_type - 1)].cget('text') and "✔✔" not in self.cal_buttons[(port - 1) * 4 + (cal_type - 1)].cget('text'):
            self.cal_buttons[(port - 1) * 4 + (cal_type - 1)].config(text="Калибровка\n[✔✔]")

    def __config_button_callback__(self):
        start_freq = float(self.start_freq_sb.get()) * (10 ** (3 * self.start_freq_units.current()))
        stop_freq = float(self.stop_freq_sb.get()) * (10 ** (3 * self.stop_freq_units.current()))
        points = int(self.points_sb.get())
        rbw = float(self.rbw_sb.get()) * (10 ** (3 * self.rbw_units.current()))
        power = int(self.power_sb.get())

        procedure_config["start_freq"] = start_freq
        procedure_config["stop_freq"] = stop_freq
        procedure_config["points"] = points
        procedure_config["rbw"] = rbw
        procedure_config["power"] = power

        self.visa_device.exec_procedure(**procedure_config)


