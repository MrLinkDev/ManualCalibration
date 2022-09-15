import tkinter as tk
import os

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

    def __init__(self):
        self.model_loader = ModelLoader()

        root = tk.Tk()

        root.geometry("840x460")
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

        self.__configure_model_frame__(self.model_frame)
        self.__configure_device_frame__(self.device_frame)
        self.__configure_params_frame__(self.params_frame)
        self.__configure_cal_frame__(self.cal_frame)

        self.model_frame.grid(row=0, column=0, padx=10, pady=10)
        self.device_frame.grid(row=1, column=0, padx=10)
        self.params_frame.grid(row=2, column=0, padx=10, pady=10)
        self.cal_frame.grid(row=0, rowspan=3, column=1, padx=10, pady=10)

    def __configure_model_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=2)

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
        frame.grid_columnconfigure(0, weight=2)

        self.info_label = ttk.Label(frame, text="Прибор:")
        self.info_label.grid(row=0, column=0, columnspan=3, sticky="nw", padx=5, pady=5)

        self.address_box = ttk.Entry(frame)
        self.address_box.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.connect_button = ttk.Button(frame, text="Подключиться", command=lambda: self.__create_visa_device__())
        self.connect_button.grid(row=1, column=2, padx=5, pady=5)

    def __configure_params_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=2)

        test_label = ttk.Label(frame, text="label_3")
        test_label.grid(row=0, column=0, sticky="nw")

    def __configure_cal_frame__(self, frame):
        frame.grid_columnconfigure(0, weight=5)

        test_label = ttk.Label(frame, text="label_4")
        test_label.grid(row=0, column=0)

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

        if self.visa_device is not None:
            self.model_label.config(state="disabled")
            self.device_list.config(state="disabled")
            self.load_label.config(state="disabled")
            self.filepath_box.config(state="disabled")
            self.filepicker_button.config(state="disabled")

            self.address_box.config(state="disabled")
            self.connect_button.config(text="Отключить", command=lambda: self.__destroy_visa_device__())

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


