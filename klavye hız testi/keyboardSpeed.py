import tkinter as tk
from tkinter import messagebox
import random
from time import time
from collections import Counter
from words import turkce_kelimeler, ingilizce_kelimeler

class KlavyeTesti:
    def __init__(self, root):
        self.root = root
        self.root.title("Klavye Hız Testi")
        self.root.geometry("800x600")

        self.start_time = None
        self.word_count = 0
        self.correct_word_count = 0
        self.incorrect_word_count = 0
        self.keystrokes = 0
        self.backspace_count = 0
        self.key_frequencies = Counter()
        self.used_words = set()

        self.current_word = ""
        self.kelimeler = []

        self.show_language_selection()

    def show_language_selection(self):
        self.language_frame = tk.Frame(self.root)
        self.language_frame.pack(expand=True)

        label = tk.Label(self.language_frame, text="Lütfen bir dil seçin", font=("Helvetica", 24))
        label.pack(pady=20)

        turkish_button = tk.Button(self.language_frame, text="Türkçe", font=("Helvetica", 20), width=15, command=self.choose_turkish)
        turkish_button.pack(pady=10)

        english_button = tk.Button(self.language_frame, text="English", font=("Helvetica", 20), width=15, command=self.choose_english)
        english_button.pack(pady=10)

    def choose_turkish(self):
        self.kelimeler = turkce_kelimeler
        self.language_frame.pack_forget()
        self.setup_ui()

    def choose_english(self):
        self.kelimeler = ingilizce_kelimeler
        self.language_frame.pack_forget()
        self.setup_ui()

    def setup_ui(self):
        self.label_timer = tk.Label(self.root, text="Süre: 60", font=("Helvetica", 24))
        self.label_timer.pack(pady=20)

        self.current_word = self.get_random_word()
        self.label_word = tk.Label(self.root, text=self.current_word, font=("Helvetica", 32))
        self.label_word.pack(pady=20)

        self.entry_input = tk.Entry(self.root, font=("Helvetica", 24), justify='center')
        self.entry_input.pack(pady=20)
        self.entry_input.bind("<KeyPress>", self.on_key_press)
        self.entry_input.bind("<Return>", self.check_word)

        self.result_text = tk.Text(self.root, height=10, font=("Helvetica", 16))
        self.result_text.pack(pady=20)
        self.result_text.config(state=tk.DISABLED)

    def start_timer(self):
        if self.start_time is None:
            self.start_time = time()
            self.update_timer()

    def update_timer(self):
        elapsed_time = int(time() - self.start_time)
        remaining_time = 60 - elapsed_time
        self.label_timer.config(text=f"Süre: {remaining_time}")

        if remaining_time > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.show_results()

    def on_key_press(self, event):
        if self.start_time is None:
            self.start_timer()

        if event.keysym == "BackSpace":
            self.backspace_count += 1
        else:
            self.keystrokes += 1
            self.key_frequencies[event.char] += 1

    def check_word(self, event):
        typed_word = self.entry_input.get().strip()
        if typed_word:
            self.word_count += 1
            if typed_word == self.current_word:
                self.correct_word_count += 1
            else:
                self.incorrect_word_count += 1
        self.entry_input.delete(0, tk.END)
        self.current_word = self.get_random_word()
        self.label_word.config(text=self.current_word)

    def get_random_word(self):
        available_words = set(self.kelimeler) - self.used_words
        if not available_words:
            self.used_words.clear()
            available_words = set(self.kelimeler)

        word = random.choice(list(available_words))
        self.used_words.add(word)
        return word

    def show_results(self):
        self.entry_input.config(state=tk.DISABLED)
        total_time = time() - self.start_time
        words_per_minute = (self.correct_word_count / total_time) * 60
        keystrokes_per_second = self.keystrokes / total_time

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Toplam Süre: {total_time:.2f} saniye\n")
        self.result_text.insert(tk.END, f"Toplam Tuş Vuruşu: {self.keystrokes}\n")
        self.result_text.insert(tk.END, f"Saniyede Tuş Vuruşu: {keystrokes_per_second:.2f}\n")
        self.result_text.insert(tk.END, f"Dakikada Kelime: {words_per_minute:.2f}\n")
        self.result_text.insert(tk.END, f"Doğru Kelime Sayısı: {self.correct_word_count}\n")
        self.result_text.insert(tk.END, f"Yanlış Kelime Sayısı: {self.incorrect_word_count}\n")
        self.result_text.insert(tk.END, f"Backspace Kullanım Sayısı: {self.backspace_count}\n")
        self.result_text.insert(tk.END, f"Tuş Frekansları:\n{self.key_frequencies}\n")
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = KlavyeTesti(root)
    root.mainloop()
