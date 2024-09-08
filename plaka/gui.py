import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
import cv2
from PIL import Image, ImageTk
import threading

# Veritabanı işlemleri
def fetch_vehicles():
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT plate FROM vehicles")
    plates = cursor.fetchall()
    conn.close()
    return plates

def fetch_fines():
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT plate, amount FROM fines")
    fines = cursor.fetchall()
    conn.close()
    return fines

def add_fine(plate, amount):
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fines (plate, amount) VALUES (?, ?)", (plate, amount))
    conn.commit()
    conn.close()

# Video işleme ve GUI güncelleme
def update_frame():
    global lbl_image, cap

    ret, frame = cap.read()
    if ret:
        # Video karelerini PIL formatına dönüştür
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv2_image)
        photo = ImageTk.PhotoImage(image=pil_image)
        
        lbl_image.config(image=photo)
        lbl_image.image = photo
        
        window.after(10, update_frame)  # 10 ms sonra tekrar çalıştır
    
    else:
        cap.release()

def update_plates():
    plates = fetch_vehicles()
    listbox_plates.delete(0, tk.END)
    for plate in plates:
        listbox_plates.insert(tk.END, plate[0])

def update_fines():
    fines = fetch_fines()
    listbox_fines.delete(0, tk.END)
    for fine in fines:
        listbox_fines.insert(tk.END, f"Plate: {fine[0]}, Amount: ${fine[1]}")

def on_plate_click(event):
    selected_plate = listbox_plates.get(tk.ACTIVE)
    amount = simpledialog.askfloat("Fine Amount", "Enter the fine amount:")
    if amount:
        add_fine(selected_plate, amount)
        update_fines()

def create_gui():
    global window, lbl_image, listbox_plates, listbox_fines, cap

    # GUI oluşturma
    window = tk.Tk()
    window.title("Vehicle License Plate Detection")

    left_frame = tk.Frame(window)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    right_frame = tk.Frame(window)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Video Gösterim Alanı
    lbl_image = tk.Label(left_frame)
    lbl_image.pack()

    # Plakalar Listesi
    listbox_plates = tk.Listbox(right_frame)
    listbox_plates.pack()

    # Cezalar Listesi
    listbox_fines = tk.Listbox(right_frame)
    listbox_fines.pack()

    listbox_plates.bind("<Double-1>", on_plate_click)

    # Video dosyasını aç
    cap = cv2.VideoCapture('videos/cars.mp4')

    # Video güncelleme işlemini başlat
    window.after(0, update_frame)

    # GUI döngüsünü başlat
    window.mainloop()

if __name__ == "__main__":
    create_gui()
