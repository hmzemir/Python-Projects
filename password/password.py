from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Listbox

# Şifreleme anahtarını oluştur veya yükle
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    return key

# Şifreleme ve çözme işlemleri
def encrypt_password(key, password):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Şifreleri dosyaya kaydetme
def save_password(site_name, encrypted_password):
    with open("passwords.txt", "a") as file:
        file.write(f"{site_name}:{encrypted_password.decode()}\n")

# Şifreleri görüntüleme
def view_passwords(key, master_password):
    correct_password = "123456"  # Ana şifre (Bu parolayı değiştirin)

    if master_password == correct_password:
        passwords_window = tk.Toplevel()
        passwords_window.title("Kayıtlı Şifreler")
        passwords_window.geometry("400x300")  # Genişlik ve yükseklik ayarları

        output = scrolledtext.ScrolledText(passwords_window, width=50, height=10)
        output.pack(pady=10)

        if os.path.exists("passwords.txt"):
            with open("passwords.txt", "r") as file:
                for line in file.readlines():
                    site_name, encrypted_password = line.strip().split(":")
                    decrypted_password = decrypt_password(key, encrypted_password.encode())
                    output.insert(tk.END, f"Site: {site_name} | Şifre: {decrypted_password}\n")
        else:
            output.insert(tk.END, "Henüz kayıtlı şifre yok.")

        close_button = tk.Button(passwords_window, text="Kapat", command=passwords_window.destroy)
        close_button.pack(pady=5)
    else:
        messagebox.showerror("Hatalı Şifre", "Girdiğiniz şifre yanlış!")

# Şifre silme işlemi
def delete_password(key, master_password):
    correct_password = "123456"  # Ana şifre (Bu parolayı değiştirin)

    if master_password == correct_password:
        delete_window = tk.Toplevel()
        delete_window.title("Şifre Sil")
        delete_window.geometry("400x300")  # Genişlik ve yükseklik ayarları

        listbox = Listbox(delete_window, width=50, height=10)
        listbox.pack(pady=10)

        if os.path.exists("passwords.txt"):
            with open("passwords.txt", "r") as file:
                passwords = file.readlines()
                for line in passwords:
                    site_name, encrypted_password = line.strip().split(":")
                    decrypted_password = decrypt_password(key, encrypted_password.encode())
                    listbox.insert(tk.END, f"Site: {site_name} | Şifre: {decrypted_password}")

            def delete_selected_password():
                selected_index = listbox.curselection()
                if selected_index:
                    del passwords[selected_index[0]]
                    with open("passwords.txt", "w") as file:
                        file.writelines(passwords)
                    listbox.delete(selected_index)
                    messagebox.showinfo("Bilgi", "Şifre silindi!")
                else:
                    messagebox.showwarning("Uyarı", "Lütfen silmek için bir şifre seçin.")

            delete_button = tk.Button(delete_window, text="Seçili Şifreyi Sil", command=delete_selected_password)
            delete_button.pack(pady=5)

        else:
            messagebox.showinfo("Bilgi", "Henüz kayıtlı şifre yok.")
            delete_window.destroy()

        close_button = tk.Button(delete_window, text="Kapat", command=delete_window.destroy)
        close_button.pack(pady=5)
    else:
        messagebox.showerror("Hatalı Şifre", "Girdiğiniz şifre yanlış!")

# Şifre kaydetme işlemi
def save_password_dialog(key):
    site_name = simpledialog.askstring("Site Adı", "Site adını girin:")
    password = simpledialog.askstring("Şifre", "Şifreyi girin:", show='*')

    if site_name and password:
        encrypted_password = encrypt_password(key, password)
        save_password(site_name, encrypted_password)
        messagebox.showinfo("Bilgi", "Şifre kaydedildi!")

# Ana GUI penceresi
def main():
    key = load_key()

    root = tk.Tk()
    root.title("Şifre Yöneticisi")
    root.geometry("300x200")  # Ana pencere genişlik ve yükseklik ayarları

    # Kaydetme butonu
    save_button = tk.Button(root, text="Şifre Kaydet", command=lambda: save_password_dialog(key))
    save_button.pack(pady=5)

    # Şifre görüntüleme butonu
    def prompt_master_password():
        master_password = simpledialog.askstring("Şifre Girişi", "Ana şifreyi girin:", show='*')
        if master_password:
            view_passwords(key, master_password)

    view_button = tk.Button(root, text="Şifreleri Görüntüle", command=prompt_master_password)
    view_button.pack(pady=5)

    # Şifre silme butonu
    def prompt_master_password_for_delete():
        master_password = simpledialog.askstring("Şifre Girişi", "Ana şifreyi girin:", show='*')
        if master_password:
            delete_password(key, master_password)

    delete_button = tk.Button(root, text="Şifre Sil", command=prompt_master_password_for_delete)
    delete_button.pack(pady=5)

    # Çıkış butonu
    exit_button = tk.Button(root, text="Çıkış", command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
