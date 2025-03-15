import cv2
import subprocess
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

# Crear ventana principal
ventana_qr = Tk()
ventana_qr.title("Sistema gestor de escaneo CCI Ingeniería")
ventana_qr.minsize(width=480, height=500)
ventana_qr.config(padx=35, pady=35)

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, ancho, alto):
    """Centra la ventana en la pantalla según el ancho y alto especificados."""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Centrar la ventana principal
centrar_ventana(ventana_qr, 300, 500)

# Inicializar captura de video
capture = cv2.VideoCapture(2)

if not capture.isOpened():
    print("No se pudo abrir la cámara.")
else:
    print("Cámara abierta correctamente.")

# Función para actualizar el video en la interfaz
def actualizar_video():
    """Captura un frame de la cámara, lo convierte y lo muestra en la interfaz gráfica."""
    ret, frame = capture.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
        frame = cv2.resize(frame, (400, 300))  # Ajustar tamaño del video
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        etiqueta_video.img_tk = img_tk  # Evitar que la imagen sea eliminada por el recolector de basura
        etiqueta_video.configure(image=img_tk)
        
        # Detectar QR en la imagen capturada
        qrDetector = cv2.QRCodeDetector()
        data, bbox, _ = qrDetector.detectAndDecode(frame)
        
        if data:
            etiqueta_resultado.config(text=f'QR Detectado: {data}', fg='green')
            # Guardar el QR detectado en un archivo de texto
            with open("detectar_qr.txt", "w") as f:
                f.write(data)
        else:
            etiqueta_resultado.config(text="No detecta", fg='red')
        
    # Llamar nuevamente a la función después de 10ms
    ventana_qr.after(10, actualizar_video)

# Función para regresar a la ventana principal
def volver_main():
    """Libera la cámara y cierra la ventana, regresando a la ventana principal."""
    capture.release()
    ventana_qr.destroy()
    subprocess.Popen(["python", "main.py"])

# Etiqueta de instrucciones
Label(ventana_qr, text="Acerque el QR al recuadro", font=("Arial", 15)).grid(column=0, row=0, pady=10)

# Etiqueta donde se mostrará el video en tiempo real
etiqueta_video = Label(ventana_qr)
etiqueta_video.grid(column=0, row=1)

# Etiqueta para mostrar el estado del escaneo del QR
etiqueta_resultado = Label(ventana_qr, text="No detecta", font=("Arial", 12), fg='red')
etiqueta_resultado.grid(column=0, row=2, pady=10)

# Botón para regresar a la ventana principal
boton_volver = Button(ventana_qr, text="Regresar", font=("Arial", 14), command=volver_main)
boton_volver.grid(column=0, row=3, pady=10)

# Iniciar la actualización del video en la interfaz
actualizar_video()

# Ejecutar la ventana principal
ventana_qr.mainloop()