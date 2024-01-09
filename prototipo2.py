import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from random import randint
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates


class GraphPage(tk.Frame):

    def __init__(self, parent, nb_points, upper_lim, title):
        # nb_points: number of points for the graph
        tk.Frame.__init__(self, parent)
        # matplotlib figure
        self.figure = Figure(figsize=(2, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        # format the x-axis to show the time
        myFmt = mdates.DateFormatter("%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        # initial x and y data
        dateTimeObj = datetime.now() + timedelta(seconds=-nb_points)
        self.x_data = [dateTimeObj + timedelta(seconds=i) for i in range(nb_points)]
        self.y_data = [0 for i in range(nb_points)]
        # create the plot
        self.plot, = self.ax.plot(self.x_data, self.y_data)
        self.ax.set_ylim(0, upper_lim)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def animate(self, new_data):
        # append new data point to the x and y data
        self.x_data.append(datetime.now())
        self.y_data.append(new_data)
        # remove oldest data point
        self.x_data = self.x_data[1:]
        self.y_data = self.y_data[1:]
        # update plot data
        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])
        self.canvas.draw_idle()  # redraw plot


class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TKINTER CON FRAME ")
        self.todos_frames = dict()
        contenedor_principal = tk.Frame(self, bg="yellow")
        contenedor_principal.grid(padx=40, pady=50, sticky="nsew")

        # Division de secciones del programa
        for F in (Frame_1, Frame_2):
            frame = F(contenedor_principal, self)
            frame.grid(row=0, column=0, sticky="nsew")  # Para inicializar sin problemas
            self.todos_frames[F] = frame
        self.show_frame(Frame_1)

    def show_frame(self, contenedor_llamado):
        frame = self.todos_frames[contenedor_llamado]
        frame.tkraise()  # la cual permite traer frame indicada a primer plano


# parent = container
class Frame_1(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.configure(bg="yellow", padx=50, pady=10)



        B_2 = ttk.Button(self, text="f2", command=lambda: controller.show_frame(Frame_2))
        B_2.grid(row=3, column=0)

        # Compile
        main = tk.Frame(self, background="red", height=20)
        main.grid(row=4, column=0, sticky="nsew")

        graph1 = GraphPage(main, 75, 1200, "Altitude")
        graph2 = GraphPage(main, 75, 50, "Temperature")
        graph3 = GraphPage(main, 75, 110, "Battery voltage")
        graph4 = GraphPage(main, 75, 1500, "Pressure")
        # Ordenar graficos
        graph1.grid(row=0, column=0, sticky="nsew")
        graph2.grid(row=0, column=1, sticky="nsew")
        graph3.grid(row=1, column=0, sticky="nsew")
        graph4.grid(row=1, column=1, sticky="nsew")

        # Habilitar escalado de tamaño de los graficos
        main.columnconfigure(tuple(range(2)), weight=1)
        main.rowconfigure(tuple(range(2)), weight=1)

        # Habilitar escalado de tamaño del display de datos
        self.columnconfigure(tuple(range(5)), weight=1)
        self.rowconfigure(tuple(range(2)), weight=1)

        # Data extra
        labels = []
        names = ["TeamID", "Mission time", "Packet count", "Altitude", "Temperature", "Angle X", "Angle Y",
                 "Battery voltage", "Pressure"]
        values = [0 for i in range(len(names))]
        for i in range(len(names)):
            label = tk.Label(self, text=names[i] + ": " + str(values[i]), font=("Arial", 15), bg="#FFFFFF")
            labels.append(label)
            match i:
                case 0:
                    labels[i].grid(row=5, column=0, sticky="nsew")
                case 1:
                    labels[i].grid(row=5, column=1, sticky="nsew")
                case 2:
                    labels[i].grid(row=5, column=2, sticky="nsew")
                case 3:
                    labels[i].grid(row=5, column=3, sticky="nsew")
                case 4:
                    labels[i].grid(row=5, column=4, sticky="nsew")
                case 5:
                    labels[i].grid(row=6, column=0, sticky="nsew")
                case 6:
                    labels[i].grid(row=6, column=1, sticky="nsew")
                case 7:
                    labels[i].grid(row=6, column=2, sticky="nsew")
                case 8:
                    labels[i].grid(row=6, column=3, sticky="nsew")

        def update_label(alti, temp, volt, pres):
            for i in range(len(names)):
                match i:
                    case 0:
                        values[i] = 100
                    case 1:
                        values[i] += 1
                    case 2:
                        values[i] = 10
                    case 3:
                        values[i] = alti
                    case 4:
                        values[i] = temp
                    case 5:
                        values[i] = randint(-35, 35)
                    case 6:
                        values[i] = randint(-35, 35)
                    case 7:
                        values[i] = volt
                    case 8:
                        values[i] = pres
                labels[i].config(text=names[i] + ": " + str(values[i]))

        # Iniciar las animaciones
        altitud = 100
        temp = 25
        voltage = 100
        presion = 760

        def update():
            nonlocal altitud, temp, voltage, presion

            altitud += randint(-5, 5)
            temp += randint(-2, 2)
            if randint(0, 100) > 95:
                voltage -= 1
            presion += randint(-5, 5)

            graph1.animate(altitud)
            graph2.animate(temp)
            graph3.animate(voltage)
            graph4.animate(presion)
            update_label(altitud, temp, voltage, presion)
            self.after(1000, update)

        update()


class Frame_2(tk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.configure(bg="yellow", padx=50, pady=10)



        B_2 = ttk.Button(self, text="f1", command=lambda: controller.show_frame(Frame_1))
        B_2.grid(row=3, column=0)

        # Compile
        main = tk.Frame(self, background="red", height=20)
        main.grid(row=4, column=0, sticky="nsew")

        graph1 = GraphPage(main, 75, 1200, "Altitude")

        # Ordenar graficos
        graph1.grid(row=0, column=0, sticky="nsew")


        # Habilitar escalado de tamaño de los graficos
        main.columnconfigure(tuple(range(2)), weight=1)
        main.rowconfigure(tuple(range(2)), weight=1)

        # Habilitar escalado de tamaño del display de datos
        self.columnconfigure(tuple(range(5)), weight=1)
        self.rowconfigure(tuple(range(2)), weight=1)

        # Data extra
        labels = []
        names = ["TeamID", "Mission time", "Packet count", "Altitude", "Temperature", "Angle X", "Angle Y",
                 "Battery voltage", "Pressure"]
        values = [0 for i in range(len(names))]
        for i in range(len(names)):
            label = tk.Label(self, text=names[i] + ": " + str(values[i]), font=("Arial", 15), bg="#FFFFFF")
            labels.append(label)
            match i:
                case 0:
                    labels[i].grid(row=5, column=0, sticky="nsew")
                case 1:
                    labels[i].grid(row=5, column=1, sticky="nsew")
                case 2:
                    labels[i].grid(row=5, column=2, sticky="nsew")
                case 3:
                    labels[i].grid(row=5, column=3, sticky="nsew")
                case 4:
                    labels[i].grid(row=5, column=4, sticky="nsew")
                case 5:
                    labels[i].grid(row=6, column=0, sticky="nsew")
                case 6:
                    labels[i].grid(row=6, column=1, sticky="nsew")
                case 7:
                    labels[i].grid(row=6, column=2, sticky="nsew")
                case 8:
                    labels[i].grid(row=6, column=3, sticky="nsew")

        def update_label(alti, temp, volt, pres):
            for i in range(len(names)):
                match i:
                    case 0:
                        values[i] = 100
                    case 1:
                        values[i] += 1
                    case 2:
                        values[i] = 10
                    case 3:
                        values[i] = alti
                    case 4:
                        values[i] = temp
                    case 5:
                        values[i] = randint(-35, 35)
                    case 6:
                        values[i] = randint(-35, 35)
                    case 7:
                        values[i] = volt
                    case 8:
                        values[i] = pres
                labels[i].config(text=names[i] + ": " + str(values[i]))

        # Iniciar las animaciones
        altitud = 100
        temp = 25
        voltage = 100
        presion = 760

        def update():
            nonlocal altitud, temp, voltage, presion

            altitud += randint(-5, 5)
            temp += randint(-2, 2)
            if randint(0, 100) > 95:
                voltage -= 1
            presion += randint(-5, 5)

            graph1.animate(altitud)

            update_label(altitud, temp, voltage, presion)
            self.after(1000, update)

        update()



root = APP()
root.mainloop()
