import tkinter as tk
import threading
import pyautogui
import keyboard
import time

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")

        self.clicking = False
        self.click_key = None
        self.interval = 0.1

        self.create_widgets()

    def create_widgets(self):
        # Tuş atama butonu
        self.key_label = tk.Label(self.root, text="Assigned Key: None")
        self.key_label.pack(pady=10)

        self.assign_button = tk.Button(self.root, text="Assign Key", command=self.assign_key)
        self.assign_button.pack(pady=10)

        # Tıklama sayısı girişi
        self.interval_label = tk.Label(self.root, text="Clicks Per Second:")
        self.interval_label.pack(pady=10)

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack(pady=10)

        # Durum etiketi
        self.status_label = tk.Label(self.root, text="Status: Idle")
        self.status_label.pack(pady=10)

    def assign_key(self):
        self.key_label.config(text="Press any key...")
        self.root.update()

        key = keyboard.read_event()
        if key.event_type == keyboard.KEY_DOWN:
            self.click_key = key.name
            self.key_label.config(text=f"Assigned Key: {self.click_key}")

            # Başlatma ve durdurma için tuş olayını ayarla
            keyboard.add_hotkey(self.click_key, self.toggle_clicking)

    def toggle_clicking(self):
        if self.clicking:
            self.clicking = False
            self.status_label.config(text="Status: Stopped")
        else:
            self.clicking = True
            self.status_label.config(text="Status: Clicking")
            try:
                self.interval = 1 / float(self.interval_entry.get())
            except ValueError:
                self.interval = 0.1

            threading.Thread(target=self.start_clicking, daemon=True).start()

    def start_clicking(self):
        while self.clicking:
            pyautogui.click()
            time.sleep(self.interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
