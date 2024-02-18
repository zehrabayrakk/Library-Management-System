import tkinter as tk
from tkinter import messagebox

class Library:
    def __init__(self, filename="books.txt"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(self.filename, "w") as file:
            for book in self.books:
                file.write(f"{book}\n")

    def list_books(self):
        if not self.books:
            return "Kütüphanede kitap bulunmamaktadır."
        result = ""
        for book in self.books:
           title, author, release_year, pages = book.split(',')
           result += f"Başlık: {title}\n"
           result += f"Yazar: {author}\n"
           result += f"Yayın Yılı: {release_year}\n"
           result += f"Sayfa Sayısı: {pages}\n\n"
        return result

    def add_book(self, title, author, release_year, pages):
        self.books.append(f"{title},{author},{release_year},{pages}")
        self.save_books()

    def remove_book(self, title_to_remove):
        self.books = [book for book in self.books if not book.split(',')[0] == title_to_remove]
        self.save_books()

    def search_books(self, search_query):
        found_books = [book for book in self.books if search_query in book.lower()]
        if found_books:
            result = "Kütüphanede bulunan kitaplar:\n"
            for book in found_books:
                title, author, release_year, pages = book.split(',')
                result += f"Başlık: {title}, Yazar: {author}, Yayın Yılı: {release_year}, Sayfa Sayısı: {pages}\n"
            return result
        else:
            return "Arama kriterlerinize uygun kitap bulunamadı."

class LibraryGUI:
    def __init__(self, master):
        self.master = master
        master.title("Kütüphane Yönetim Sistemi")
        master.geometry("500x720")

        self.label = tk.Label(master, text="Kütüphane Yönetim Sistemi", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        self.label.pack(pady=(10, 20))

        self.button_bg = "#4CAF50"
        self.button_fg = "white"
        self.button_width = 20
        self.button_height = 2

        self.list_button = tk.Button(master, text="Kitapları Listele", command=self.list_books, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.list_button.pack(pady=(0, 10))

        self.add_button = tk.Button(master, text="Kitap Ekle", command=self.open_add_book_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.add_button.pack(pady=(0, 10))

        self.remove_button = tk.Button(master, text="Kitap Çıkart", command=self.open_remove_book_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.remove_button.pack(pady=(0, 10))

        self.search_button = tk.Button(master, text="Kitap Arama", command=self.open_search_book_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.search_button.pack(pady=(0, 10))

        self.quit_button = tk.Button(master, text="Çıkış Yap", command=self.confirm_exit, bg="#ff5722", fg="white", width=self.button_width, height=self.button_height)
        self.quit_button.pack(pady=(0, 20))

        self.result_text = tk.Text(master, wrap=tk.WORD, width=50, height=20, relief=tk.GROOVE, bg="#f0f0f0", font=("Helvetica", 12))
        self.result_text.pack()

        self.lib = Library()

    def list_books(self):
        books = self.lib.list_books()
        self.update_result_text(books)

    def add_book(self, title, author, release_year, pages):
        self.lib.add_book(title, author, release_year, pages)
        self.update_result_text("Kitap başarıyla eklendi.")

    def remove_book(self, title_to_remove):
        self.lib.remove_book(title_to_remove)
        self.update_result_text("Kitap başarıyla çıkarıldı.")

    def search_books(self, search_query):
        result = self.lib.search_books(search_query)
        self.update_result_text(result)

    def clear_result_text(self):
        self.result_text.delete(1.0, tk.END)

    def update_result_text(self, text):
        self.clear_result_text()
        self.result_text.insert(tk.END, text)

    def open_add_book_window(self):
        self.add_book_window = tk.Toplevel(self.master)
        self.add_book_window.title("Kitap Ekle")
        self.add_book_window.geometry("400x300")

        label_font = ("Helvetica", 12)

        self.title_label = tk.Label(self.add_book_window, text="Kitap Adı:", font=label_font)
        self.title_label.pack()

        self.title_entry = tk.Entry(self.add_book_window, font=label_font)
        self.title_entry.pack()

        self.author_label = tk.Label(self.add_book_window, text="Yazar:", font=label_font)
        self.author_label.pack()

        self.author_entry = tk.Entry(self.add_book_window, font=label_font)
        self.author_entry.pack()

        self.release_year_label = tk.Label(self.add_book_window, text="Yayın Yılı:", font=label_font)
        self.release_year_label.pack()

        self.release_year_entry = tk.Entry(self.add_book_window, font=label_font)
        self.release_year_entry.pack()

        self.pages_label = tk.Label(self.add_book_window, text="Sayfa Sayısı:", font=label_font)
        self.pages_label.pack()

        self.pages_entry = tk.Entry(self.add_book_window, font=label_font)
        self.pages_entry.pack()

        self.add_button = tk.Button(self.add_book_window, text="Kitap Ekle", command=self.add_book_from_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.add_button.pack()

    def add_book_from_window(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        release_year = self.release_year_entry.get()
        pages = self.pages_entry.get()
        if title and author and release_year and pages:
            self.add_book(title, author, release_year, pages)
            self.add_book_window.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

    def open_remove_book_window(self):
        self.remove_book_window = tk.Toplevel(self.master)
        self.remove_book_window.title("Kitap Çıkart")
        self.remove_book_window.geometry("300x150")

        label_font = ("Helvetica", 12)

        self.title_label = tk.Label(self.remove_book_window, text="Silmek İstediğiniz Kitabın Adı:", font=label_font)
        self.title_label.pack()

        self.title_entry = tk.Entry(self.remove_book_window, font=label_font)
        self.title_entry.pack()

        self.remove_button = tk.Button(self.remove_book_window, text="Kitap Çıkart", command=self.remove_book_from_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.remove_button.pack()

    def remove_book_from_window(self):
        title = self.title_entry.get()
        if title:
            self.remove_book(title)
            self.remove_book_window.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen bir kitap adı girin.")

    def open_search_book_window(self):
        self.search_book_window = tk.Toplevel(self.master)
        self.search_book_window.title("Kitap Arama")
        self.search_book_window.geometry("300x150")

        label_font = ("Helvetica", 12)

        self.search_label = tk.Label(self.search_book_window, text="Aramak İstediğiniz Kitap veya Yazar:", font=label_font)
        self.search_label.pack()

        self.search_entry = tk.Entry(self.search_book_window, font=label_font)
        self.search_entry.pack()

        self.search_button = tk.Button(self.search_book_window, text="Kitap Ara", command=self.search_book_from_window, bg=self.button_bg, fg=self.button_fg, width=self.button_width, height=self.button_height)
        self.search_button.pack()

    def search_book_from_window(self):
        query = self.search_entry.get()
        if query:
            self.search_books(query)
            self.search_book_window.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen bir arama terimi girin.")

    def confirm_exit(self):
        if messagebox.askokcancel("Çıkış", "Programı kapatmak istediğinizden emin misiniz?"):
            self.master.destroy()

root = tk.Tk()
app = LibraryGUI(root)
root.mainloop()
