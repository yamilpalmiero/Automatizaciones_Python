import tkinter as tk
import pyautogui
import threading
import time
import os

# Variable de control
running = False

# Movimiento perceptible del mouse
def mover_mouse():
    global running
    while running:
        current_x, current_y = pyautogui.position()
        pyautogui.moveTo(current_x + 50, current_y, duration=0.2)
        time.sleep(1)
        pyautogui.moveTo(current_x, current_y, duration=0.2)
        time.sleep(10)

# Iniciar el movimiento
def iniciar():
    global running
    if not running:
        running = True
        threading.Thread(target=mover_mouse, daemon=True).start()
        estado_label.config(text="Estado: Activo", fg="green")

# Detener el movimiento
def detener():
    global running
    running = False
    estado_label.config(text="Estado: Detenido", fg="red")

# Crear la interfaz de usuario
ventana = tk.Tk()
ventana.title("Sneaky Mouse")
ventana.geometry("300x150")

# Establecer ícono
icon_path = os.path.join("img", "sneaky_mouse_icon.ico")
if os.path.exists(icon_path):
    ventana.iconbitmap(icon_path)
else:
    print("⚠️ Advertencia: ícono no encontrado en img/sneaky_mouse_icon.ico")

# Widgets
titulo_label = tk.Label(ventana, text="Sneaky Mouse", font=("Helvetica", 16, "bold"))
titulo_label.pack(pady=10)

estado_label = tk.Label(ventana, text="Estado: Detenido", fg="red", font=("Helvetica", 12))
estado_label.pack()

boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar, bg="green", fg="white", width=12)
boton_iniciar.pack(pady=5)

boton_detener = tk.Button(ventana, text="Detener", command=detener, bg="red", fg="white", width=12)
boton_detener.pack(pady=5)

# Ejecutar la ventana principal
ventana.mainloop()
