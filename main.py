import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox as mb
from tkinter import Entry, ttk, Tk
import numpy as np
from scipy import signal
from scipy.fft import fft
def main():
    root = Tk()
    gui = Interface(root)
    gui.root.mainloop()

class Interface:

    def __init__(self, root):
        self.root = root
        self.root.geometry('980x680')
        self.root.title("Analizador de Señales")

        self.amplitude = 1.0
        self.frequency = 60
        self.offset = 0.0
        self.phase = 0.0
        self.frequency_m = 2000
        self.sample_number = 50

        self.title = ttk.Label(self.root, text="Gráfica de Señales", font="bold")
        self.title.place(x=500, y=5)

        self.plot_sin()

        # ------------ Select Signal --------------------
        self.select_label = ttk.Label(self.root, text="Selecciona la Señal").place(x=20, y=20)
        self.select = ttk.Combobox(self.root, values=["Seno", "Rectangular", "Triangular"])
        self.select.place(x=20, y=40)
        self.select.current(0)

        # ----------- Input Amplitude ------------------
        self.title_amp = ttk.Label(self.root, text="Amplitud").place(x=20, y=80)
        self.amplitude_get = Entry(self.root)
        self.amplitude_get.place(x=20, y=100)

        # ----------- Input Frequency ------------------
        self.title_frec = ttk.Label(self.root, text="Frecuencia").place(x=20, y=150)
        self.frequency_get = Entry(self.root)
        self.frequency_get.place(x=20, y=170)

        # ----------- Input Phase ------------------
        self.title_ph = ttk.Label(self.root, text="Fase").place(x=20, y=210)
        self.phase_get = Entry(self.root)
        self.phase_get.place(x=20, y=230)

        # ----------- Input OffSet ------------------
        self.title_os = ttk.Label(self.root, text="OffSet").place(x=20, y=270)
        self.offset_get = Entry(self.root)
        self.offset_get.place(x=20, y=290)

        # ----------- Input Sample Frequency ------------------
        self.title_fs = ttk.Label(self.root, text="Frecuencia de Muestreo").place(x=20, y=330)
        self.sampleF_get = Entry(self.root)
        self.sampleF_get.place(x=20, y=350)

        # ----------- Input Sample Number ------------------
        self.title_sn = ttk.Label(self.root, text="Número de Muestras").place(x=20, y=390)
        self.samplen_get = Entry(self.root)
        self.samplen_get.place(x=20, y=410)

        # -------------- Buttons ---------------------------
        self.generate = ttk.Button(self.root, text="Generar", command=self.update)
        self.generate.place(x=20, y=600)
        self.generate = ttk.Button(self.root, text="Salir", command=root.destroy)
        self.generate.place(x=110, y=600)

    def cell_empty(self):

        amplitude = self.amplitude_get.get() == ""
        frequency = self.frequency_get.get() == ""
        phase = self.phase_get.get() == ""
        offset = self.offset_get.get() == ""
        sample_F = self.sampleF_get.get() == ""
        sample_n = self.samplen_get.get() == ""

        if amplitude or frequency or phase or offset or sample_F or sample_n:
            return True

        else:
            return False

    def update(self, event=None):
        if not self.cell_empty():
            self.amplitude = float(self.amplitude_get.get())
            self.frequency = int(self.frequency_get.get())
            self.phase = float(self.phase_get.get())
            self.frequency_m = int(self.sampleF_get.get())
            self.offset = float(self.offset_get.get())
            self.sample_number = int(self.samplen_get.get())
            self.root.bind("<Return>", self.update)
            self.changeSignal()

        else:
            mb.showerror("Cuidado", "No puede dejar los cuadros de entrada de números vacíos")

    def changeSignal(self):
        if self.select.get() == 'Seno':
            self.plot_sin()

        elif self.select.get() == 'Triangular':
            self.plot_sawtooth()

        elif self.select.get() == 'Rectangular':
            self.plot_rect()

    def plot_sin(self):
        sin = lambda n: self.amplitude * np.sin(2 * np.pi * self.frequency * n + self.phase * np.pi / 180) + self.offset
        t = np.linspace(0.0, self.sample_number * 1 / self.frequency_m, self.sample_number, endpoint=False)

        # ---------------------- Grafica--------
        self.plotFreq_fun(sin(t))

        figure = plt.figure(figsize=(7.5, 4), dpi=80)
        figure.add_subplot().plot(t, sin(t), '-*',
                                  label="RMS: {}\n Valor Medio: {}".format(round(self.rmsValue(sin(t)), 3),
                                                                           round(np.mean(sin(t)), 3)))

        chart = FigureCanvasTkAgg(figure, self.root)
        chart.get_tk_widget().place(x=250, y=30)
        plt.title("Función Seno")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.grid()

    def plotFreq_fun(self, fun):
        fun_freq = 2 / self.sample_number * np.abs(fft(fun)[0:self.sample_number // 2])

        figure = plt.figure(figsize=(7.5, 3.5), dpi=80)
        figure.add_subplot().plot(fun_freq)

        chart = FigureCanvasTkAgg(figure, self.root)
        chart.get_tk_widget().place(x=250, y=340)

        plt.xlabel("Armónico Frecuencia")
        plt.ylabel("Amplitud")
        plt.grid()

    def plot_sawtooth(self):
        saw = lambda n: self.amplitude * signal.sawtooth(
            2 * np.pi * self.frequency * n + self.phase * np.pi / 180) + self.offset
        t = np.linspace(0.0, self.sample_number * 1 / self.frequency_m, self.sample_number, endpoint=False)

        self.plotFreq_fun(saw(t))

        figure = plt.figure(figsize=(7.5, 4), dpi=80)
        figure.add_subplot().plot(t, saw(t), '-.',
                                  label="RMS: {}\n Valor Medio: {}".format(round(self.rmsValue(saw(t)), 3),
                                                                           round(np.mean(saw(t)), 3)))

        chart = FigureCanvasTkAgg(figure, self.root)
        chart.get_tk_widget().place(x=250, y=30)
        plt.title("Función Triangular")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.legend()
        plt.grid()

    def plot_rect(self):
        rect = lambda n: self.amplitude * signal.square(
            2 * np.pi * self.frequency * n + self.phase * np.pi / 180) + self.offset
        t = np.linspace(0.0, self.sample_number * 1 / self.frequency_m, self.sample_number, endpoint=False)

        self.plotFreq_fun(rect(t))
        figure = plt.figure(figsize=(7.5, 4), dpi=80)
        figure.add_subplot().plot(t, rect(t), '-.',
                                  label="RMS: {}\n Valor Medio: {}".format(round(self.rmsValue(rect(t)), 3),
                                                                           round(np.mean(rect(t)), 3)))
        chart = FigureCanvasTkAgg(figure, self.root)
        chart.get_tk_widget().place(x=250, y=30)
        plt.title("Función Rectangular")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.grid()
        plt.legend()

    def rmsValue(self, array):
        quad_array = array ** 2
        rms = np.sqrt(np.mean(quad_array))
        return rms


if __name__ == '__main__':
    main()