import tkinter as tk


def main():
    window = tk.Tk()

    frame = tk.Frame(master=window, width=800, height=600)
    frame.pack()

    test_label = tk.Label(master=frame, text="test label")
    test_label.place(x=300, y=200)

    window.mainloop()

