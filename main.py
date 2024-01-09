from Graphs import *
from  Data import *
import tkinter as tk
from datetime import datetime, timedelta
from random import randint

import threading
# Crear una instancia de la clase Data con el puerto serial adecuado
data_ = Data(port="/dev/ttyUSB0", baudrate=9600)  # Ajusta el puerto serial según tu configuración

# Crear ventana
root = tk.Tk()
root.geometry("1600x900") 

#Division de secciones del programa
left_toolbar = tk.Frame(background="green", width=300)
main = tk.Frame(background="red", height=20)
bottom = tk.Frame(background="blue", height=200)

# Graficos de pestaña principal
graph1 = GraphPage(main, 75, data_.altitud_list, data_.Mission_time)
graph2 = GraphPage(main, 75, data_.temperature_list, data_.Mission_time)
graph3 = GraphPage(main, 75, data_.voltage_list, data_.Mission_time)
graph4 = GraphPage(main, 75, data_.pressure_list, data_.Mission_time)

# Ordenar graficos
graph1.grid(row = 0, column = 0, sticky="nsew")
graph2.grid(row = 0, column = 1, sticky="nsew")
graph3.grid(row = 1, column = 0, sticky="nsew")
graph4.grid(row = 1, column = 1, sticky="nsew")

# Habilitar escalado de tamaño de los graficos
main.columnconfigure(tuple(range(2)), weight=1)
main.rowconfigure(tuple(range(2)), weight=1)

# Habilitar escalado de tamaño del display de datos
bottom.columnconfigure(tuple(range(5)), weight=1)
bottom.rowconfigure(tuple(range(2)), weight=1)

# Data extra
labels = []
names = ["TeamID", "Mission time","Packet count", "Altitude", "Temperature", "Angle X", "Angle Y", "Battery voltage", "Pressure"]
values = [0 for i in range(len(names))]
for i in range(len(names)):
    label = tk.Label(bottom, text=names[i] + ": " + str(values[i]), font=("Arial", 15), bg="#FFFFFF")
    labels.append(label)
    match i:
        case 0:
            labels[i].grid(row = 0, column = 0, sticky="nsew")
        case 1:
            labels[i].grid(row = 0, column = 1, sticky="nsew")
        case 2:
            labels[i].grid(row = 0, column = 2, sticky="nsew")
        case 3:
            labels[i].grid(row = 0, column = 3, sticky="nsew")
        case 4:
            labels[i].grid(row = 0, column = 4, sticky="nsew")
        case 5:
            labels[i].grid(row = 1, column = 0, sticky="nsew")
        case 6:
            labels[i].grid(row = 1, column = 1, sticky="nsew")
        case 7:
            labels[i].grid(row = 1, column = 2, sticky="nsew")
        case 8:
            labels[i].grid(row = 1, column = 3, sticky="nsew")

def update_label():
    for i in range(len(names)):
        match i:
            case 0:
                values[i] = data_.TeamID_list[-1]
            case 1:
                values[i] = data_.Mission_time[-1]
            case 2:
                values[i] = data_.packetcount_list[-1]
            case 3:
                values[i] = data_.altitud_list[-1]
            case 4:
                values[i] = data_.temperature_list[-1]
            case 5:
                values[i] = data_.ang_x_list[-1]
            case 6:
                values[i] = data_.ang_y_list[-1]
            case 7:
                values[i] = data_.voltage_list[-1]
            case 8:  
                values[i] = data_.pressure_list[-1]
        labels[i].config(text=names[i] + ": " + str(values[i]))

# Compile
left_toolbar.pack(side="right", fill="y")
main.pack(side="top", fill="both", expand=True)
bottom.pack(side="top", fill="both", expand=False)

# Iniciar las animaciones

def update():
    data_.parse_data(data_.read())
    graph1.animate(data_.altitud_list)
    graph2.animate(data_.temperature_list)
    graph3.animate(data_.voltage_list_list)
    graph4.animate(data_.pressure_list)
    update_label()
    root.after(1000, update)
    
# Single threads
root.after(1000, update)
root.mainloop()


def saludo():
    tk.label(bottom, text="hola mundo ").pack()
    
def salir():
    bottom.destroy()
boton1=tk.Button(bottom , test="soy el primer boton", command=saludo, fg="red")

    
