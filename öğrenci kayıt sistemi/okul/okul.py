import os
import sys
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Veritabanı dosyasının yolunu dinamik olarak al
def get_db_path():
    if getattr(sys, 'frozen', False):
        # PyInstaller ile paketlenmişse
        return os.path.join(sys._MEIPASS, 'okul.db')
    else:
        # Geliştirme aşamasında
        return 'okul.db'

# Veritabanına bağlanma
conn = sqlite3.connect(get_db_path())
cursor = conn.cursor()

# Veritabanı tablosunu oluştur (eğer yoksa)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ogrenciler (
        ogrenci_no TEXT PRIMARY KEY,
        ad_soyad TEXT,
        telefon_no TEXT,
        e_posta TEXT,
        sinif TEXT,
        veli_adi TEXT,
        veli_numara TEXT
    )
''')
conn.commit()

# Tkinter penceresi oluşturma
root = tk.Tk()
root.title("Öğrenci Yönetim Sistemi")
root.geometry("650x550")
root.configure(bg="#f2f2f2")  # Arka plan rengi

# Fontlar ve stiller
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 12)
button_font = ("Arial", 10, "bold")
listbox_font = ("Arial", 12)
bg_color = "#ffffff"  # Giriş alanları ve butonların arka plan rengi
fg_color = "#333333"  # Metin rengi
button_bg_color = "#4CAF50"  # Butonların arka plan rengi
button_fg_color = "#ffffff"  # Butonların metin rengi

# Öğrencileri listeleme fonksiyonu
def ogrencileri_listele():
    cursor.execute('SELECT * FROM ogrenciler')
    result = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in result:
        listbox.insert(tk.END, f"{row[0]} - {row[1]}")

# Listeden öğrenci seçildiğinde üstteki alanları doldurma
def ogrenci_sec(event):
    selected_item = listbox.curselection()
    if selected_item:
        ogrenci = listbox.get(selected_item).split(" - ")[0]
        cursor.execute('SELECT * FROM ogrenciler WHERE ogrenci_no = ?', (ogrenci,))
        result = cursor.fetchone()
        
        entry_no.delete(0, tk.END)
        entry_no.insert(tk.END, result[0])
        entry_ad.delete(0, tk.END)
        entry_ad.insert(tk.END, result[1])
        entry_telefon.delete(0, tk.END)
        entry_telefon.insert(tk.END, result[2])
        entry_eposta.delete(0, tk.END)
        entry_eposta.insert(tk.END, result[3])
        entry_sinif.delete(0, tk.END)
        entry_sinif.insert(tk.END, result[4])
        entry_veli_ad.delete(0, tk.END)
        entry_veli_ad.insert(tk.END, result[5])
        entry_veli_telefon.delete(0, tk.END)
        entry_veli_telefon.insert(tk.END, result[6])

# Öğrenci ekleme fonksiyonu
def ogrenci_ekle():
    ogrenci_no = entry_no.get()
    ad_soyad = entry_ad.get()
    telefon_no = entry_telefon.get()
    e_posta = entry_eposta.get()
    sinif = entry_sinif.get()
    veli_adi = entry_veli_ad.get()
    veli_numarasi = entry_veli_telefon.get()
    
    try:
        cursor.execute('INSERT INTO ogrenciler (ogrenci_no, ad_soyad, telefon_no, e_posta, sinif, veli_adi, veli_numara) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (ogrenci_no, ad_soyad, telefon_no, e_posta, sinif, veli_adi, veli_numarasi))
        conn.commit()
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi.")
        ogrencileri_listele()
        temizle()
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Bu öğrenci numarası zaten kayıtlı.")

# Öğrenci silme fonksiyonu
def ogrenci_sil():
    selected_item = listbox.curselection()
    if selected_item:
        ogrenci = listbox.get(selected_item).split(" - ")[0]
        cursor.execute('DELETE FROM ogrenciler WHERE ogrenci_no = ?', (ogrenci,))
        conn.commit()
        messagebox.showinfo("Başarılı", "Öğrenci başarıyla silindi.")
        ogrencileri_listele()
        temizle()

# Öğrenci güncelleme fonksiyonu
def ogrenci_guncelle():
    ogrenci_no = entry_no.get()
    ad_soyad = entry_ad.get()
    telefon_no = entry_telefon.get()
    e_posta = entry_eposta.get()
    sinif = entry_sinif.get()
    veli_adi = entry_veli_ad.get()
    veli_numarasi = entry_veli_telefon.get()
    
    cursor.execute('UPDATE ogrenciler SET ad_soyad = ?, telefon_no = ?, e_posta = ?, sinif = ?, veli_adi = ?, veli_numara = ? WHERE ogrenci_no = ?',
                   (ad_soyad, telefon_no, e_posta, sinif, veli_adi, veli_numarasi, ogrenci_no))
    conn.commit()
    messagebox.showinfo("Başarılı", "Öğrenci başarıyla güncellendi.")
    ogrencileri_listele()

# Giriş alanlarını temizleme fonksiyonu
def temizle():
    entry_no.delete(0, tk.END)
    entry_ad.delete(0, tk.END)
    entry_telefon.delete(0, tk.END)
    entry_eposta.delete(0, tk.END)
    entry_sinif.delete(0, tk.END)
    entry_veli_ad.delete(0, tk.END)
    entry_veli_telefon.delete(0, tk.END)

# Öğrenci bilgilerini giriş alanları
label_no = tk.Label(root, text="Öğrenci No:", font=label_font, bg=root['bg'], fg=fg_color)
label_no.grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_no = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_no.grid(row=0, column=1, padx=10, pady=10, sticky='w')

label_ad = tk.Label(root, text="Ad Soyad:", font=label_font, bg=root['bg'], fg=fg_color)
label_ad.grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_ad = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_ad.grid(row=1, column=1, padx=10, pady=10, sticky='w')

label_telefon = tk.Label(root, text="Telefon No:", font=label_font, bg=root['bg'], fg=fg_color)
label_telefon.grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_telefon = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_telefon.grid(row=2, column=1, padx=10, pady=10, sticky='w')

label_eposta = tk.Label(root, text="E-Posta:", font=label_font, bg=root['bg'], fg=fg_color)
label_eposta.grid(row=3, column=0, padx=10, pady=10, sticky='e')
entry_eposta = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_eposta.grid(row=3, column=1, padx=10, pady=10, sticky='w')

label_sinif = tk.Label(root, text="Sınıf:", font=label_font, bg=root['bg'], fg=fg_color)
label_sinif.grid(row=4, column=0, padx=10, pady=10, sticky='e')
entry_sinif = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_sinif.grid(row=4, column=1, padx=10, pady=10, sticky='w')

label_veli_ad = tk.Label(root, text="Veli Adı:", font=label_font, bg=root['bg'], fg=fg_color)
label_veli_ad.grid(row=5, column=0, padx=10, pady=10, sticky='e')
entry_veli_ad = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_veli_ad.grid(row=5, column=1, padx=10, pady=10, sticky='w')

label_veli_telefon = tk.Label(root, text="Veli Telefon No:", font=label_font, bg=root['bg'], fg=fg_color)
label_veli_telefon.grid(row=6, column=0, padx=10, pady=10, sticky='e')
entry_veli_telefon = tk.Entry(root, font=entry_font, bg=bg_color, fg=fg_color)
entry_veli_telefon.grid(row=6, column=1, padx=10, pady=10, sticky='w')

# Öğrenci listesini görüntülemek için Listbox
listbox = tk.Listbox(root, font=listbox_font, width=50, height=10, bg=bg_color, fg=fg_color)
listbox.grid(row=0, column=2, rowspan=7, padx=20, pady=20, sticky='ns')
listbox.bind("<<ListboxSelect>>", ogrenci_sec)

# Butonlar
button_ekle = tk.Button(root, text="Ekle", font=button_font, bg=button_bg_color, fg=button_fg_color, command=ogrenci_ekle)
button_ekle.grid(row=7, column=0, padx=10, pady=10)

button_sil = tk.Button(root, text="Sil", font=button_font, bg=button_bg_color, fg=button_fg_color, command=ogrenci_sil)
button_sil.grid(row=7, column=1, padx=10, pady=10)

button_guncelle = tk.Button(root, text="Güncelle", font=button_font, bg=button_bg_color, fg=button_fg_color, command=ogrenci_guncelle)
button_guncelle.grid(row=7, column=2, padx=10, pady=10)

button_temizle = tk.Button(root, text="Temizle", font=button_font, bg=button_bg_color, fg=button_fg_color, command=temizle)
button_temizle.grid(row=8, column=0, padx=10, pady=10)

# İlk listeleme
ogrencileri_listele()

# Ana döngü
root.mainloop()

# Veritabanı bağlantısını kapat
conn.close()
