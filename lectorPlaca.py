import cv2
import pytesseract
import re
import tkinter as tk
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk
import threading
import subprocess

# Configurar Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

class DetectorPlacas:
    def __init__(self, root, max_lecturas=150):
        self.root = root
        self.root.title("Detector de Placas")
        self.root.geometry("900x600")
        centrar_ventana(self.root, 900, 600)
        
        self.max_lecturas = max_lecturas  # Límite de lecturas antes de reiniciar
        self.contador_lecturas = 0  # Contador de lecturas válidas
        
        # Marco para los botones
        self.frame_botones = Frame(self.root)
        self.frame_botones.pack(pady=10)

        # Elementos de la interfaz
        self.label_video = Label(self.root)
        self.label_video.pack()

        self.label_placa = Label(self.root, text="Placa detectada:", font=("Arial", 14))
        self.label_placa.pack()

        self.text_placa = Label(self.root, text="Esperando...", font=("Arial", 16, "bold"), fg="green")
        self.text_placa.pack()

        self.btn_regresar = Button(self.frame_botones, text="Regresar", command=self.volver_main)
        self.btn_regresar.grid(row=0, column=0, padx=5)

        self.cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # Captura de video al iniciar
        self.ejecutando = True  # Estado de ejecución
        self.ultima_placa = ""  # Última placa detectada
        threading.Thread(target=self.actualizar_video, daemon=True).start()

    def volver_main(self):
        self.cap.release()
        self.root.destroy()
        subprocess.Popen(["Python", "main.py"])

    def es_placa_valida(self, texto):
        texto = texto.upper().strip()
        texto = re.sub(r'[^A-Z0-9-]', '', texto)
        if 6 <= len(texto) <= 8 and re.match(r'^[A-Z0-9-]+$', texto):
            return texto
        return None

    def detectar_placa(self, frame):
        alto, ancho, _ = frame.shape
        Ejex1, Ejex2 = int(ancho * 0.2), int(ancho * 0.8)
        Ejey1, Ejey2 = int(alto * 0.25), int(alto * 0.75)

        cv2.rectangle(frame, (Ejex1, Ejey1), (Ejex2, Ejey2), (0, 255, 0), 3)
        recortar = frame[Ejey1:Ejey2, Ejex1:Ejex2]
        gris = cv2.cvtColor(recortar, cv2.COLOR_BGR2GRAY)
        umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        contornos, _ = cv2.findContours(umbral, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)

        for contorno in contornos:
            perimetro = cv2.arcLength(contorno, True)
            aprox = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)

            if len(aprox) == 4:
                x, y, w, h = cv2.boundingRect(aprox)
                xpi, ypi = x + Ejex1, y + Ejey1
                xpf, ypf = x + w + Ejex1, y + h + Ejey1

                cv2.rectangle(frame, (xpi, ypi), (xpf, ypf), (255, 255, 0), 3)
                placa = frame[ypi:ypf, xpi:xpf]
                placa_gris = cv2.cvtColor(placa, cv2.COLOR_BGR2GRAY)
                _, placa_bin = cv2.threshold(placa_gris, 150, 255, cv2.THRESH_BINARY)

                if placa.shape[0] >= 36 and placa.shape[1] >= 82:
                    texto = pytesseract.image_to_string(placa_bin, config="--psm 7 --oem 3").strip()
                    return self.es_placa_valida(texto)
        return None

    def actualizar_video(self):
        while self.ejecutando:
            ret, frame = self.cap.read()
            if not ret:
                break

            nueva_placa = self.detectar_placa(frame)
            if nueva_placa:
                if nueva_placa != self.ultima_placa:
                    self.ultima_placa = nueva_placa
                    self.text_placa.config(text=nueva_placa)
                    self.guardar_placa(nueva_placa)
                    self.contador_lecturas += 1
                    if self.contador_lecturas >= self.max_lecturas:
                        self.contador_lecturas = 0
                        self.ultima_placa = ""
            else:
                self.ultima_placa = ""
                self.text_placa.config(text="No detecta", fg="red", font=("Arial", 14))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            self.label_video.config(image=img)
            self.label_video.image = img

        self.cap.release()
        self.label_video.config(image="")

    def guardar_placa(self, placa):
        with open("detectar_placas.txt", "w") as archivo:
            archivo.write(placa + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorPlacas(root, max_lecturas=150)
    root.mainloop()
