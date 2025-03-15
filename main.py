from tkinter import *
import subprocess



ventana_main = Tk()
ventana_main.title("Sistema gestor de escaneo CCI Ingeniería")
ventana_main.minsize(width=680, height=350)
ventana_main.config(padx=35, pady=35)

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

centrar_ventana(ventana_main, 680, 350)

# Función para abrir el archivo de escaneo de placas
def abrir_escaner_placa():
    ventana_main.destroy()
    subprocess.Popen(["python", "lectorPlaca.py"])
    
def abrir_escaner_Qr():
    ventana_main.destroy()
    subprocess.Popen(["python", "lectorQR.py" ])

# Etiqueta de bienvenida
Label1 = Label(ventana_main, text="¡Bienvenido!\nSistema gestor de escaneo de placas de CCI", font=("Arial", 20))
Label1.grid(column=0, row=0, columnspan=2, pady=20)

# Etiqueta de instrucción
label2 = Label(ventana_main, text="Escoja el tipo de escaneo que desea realizar", font=("Arial", 15))
label2.grid(column=0, row=1, columnspan=2, pady=30)

# Botones de opciones
boton1 = Button(ventana_main, text="Escanear Placa", font=("Arial", 14), command=abrir_escaner_placa)
boton1.grid(column=0, row=2, padx=20, pady=10)

boton2 = Button(ventana_main, text="Escanear QR", font=("Arial", 14), command=abrir_escaner_Qr)
boton2.grid(column=1, row=2, padx=20, pady=10)

ventana_main.mainloop()