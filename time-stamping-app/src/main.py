import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import queue
from rfid_reader import RfidReader
from attendance_tracker import AttendanceTracker
import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID Attendance Tracker")
        self.root.geometry("600x400")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 16), background="#2c3e50", foreground="white")
        self.style.configure("TFrame", background="#2c3e50")

        self.main_menu()

        self.attendance_tracker = AttendanceTracker()
        self.callback_queue = queue.Queue()
        self.rfid_reader = RfidReader(self.callback_queue)

        self.start_reading()
        self.check_queue()

    def main_menu(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="RFID Attendance Tracker", font=("Helvetica", 20)).pack(pady=20)
        self.create_button(frame, "Регистрация времени", self.registration_screen).pack(pady=10)
        self.create_button(frame, "Просмотр данных", self.view_data_screen).pack(pady=10)
        self.create_button(frame, "Подсчет времени", self.calculate_hours_screen).pack(pady=10)
        self.create_button(frame, "Редактирование данных", self.edit_data_screen).pack(pady=10)

    def registration_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        self.label = ttk.Label(frame, text="Приложите RFID-карту для регистрации времени...")
        self.label.pack(pady=20)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

    def view_data_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Выберите дату для просмотра данных", font=("Helvetica", 20)).pack(pady=20)
        date_entry = tk.Entry(frame, font=("Helvetica", 16))
        date_entry.pack(pady=10)
        self.create_button(frame, "Показать данные", lambda: self.show_data(date_entry.get())).pack(pady=10)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

    def show_data(self, date_str):
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text=f"Данные о посещениях за {date_str}", font=("Helvetica", 20)).pack(pady=20)
        text = tk.Text(frame, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 12))
        text.pack(pady=10)
        self.create_button(frame, "Назад", self.view_data_screen).pack(pady=10)

        attendance_data = self.attendance_tracker.get_attendance(date)
        text.insert(tk.END, "".join(attendance_data))

    def calculate_hours_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Введите месяц для подсчета времени (ГГГГ-ММ)", font=("Helvetica", 20)).pack(pady=20)
        month_entry = tk.Entry(frame, font=("Helvetica", 16))
        month_entry.pack(pady=10)
        self.create_button(frame, "Показать данные", lambda: self.show_hours(month_entry.get())).pack(pady=10)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

    def show_hours(self, month_str):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text=f"Отработанные часы за {month_str}", font=("Helvetica", 20)).pack(pady=20)
        text = tk.Text(frame, wrap=tk.WORD, width=50, height=20, font=("Helvetica", 12))
        text.pack(pady=10)
        self.create_button(frame, "Назад", self.calculate_hours_screen).pack(pady=10)

        hours_worked = self.attendance_tracker.calculate_hours(month_str)
        data = ""
        for uid, hours in hours_worked.items():
            name = self.attendance_tracker.uid_to_name.get(uid, "Неизвестный")
            data += f"{name} (UID: {uid}) отработал {hours:.2f} часов\n"
        text.insert(tk.END, data)

    def edit_data_screen(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Редактирование данных", font=("Helvetica", 20)).pack(pady=20)
        ttk.Label(frame, text="Дата (ГГГГ-ММ-ДД):", font=("Helvetica", 16)).pack(pady=5)
        date_entry = tk.Entry(frame, font=("Helvetica", 16))
        date_entry.pack(pady=5)
        ttk.Label(frame, text="Старое значение:", font=("Helvetica", 16)).pack(pady=5)
        old_entry = tk.Entry(frame, font=("Helvetica", 16))
        old_entry.pack(pady=5)
        ttk.Label(frame, text="Новое значение:", font=("Helvetica", 16)).pack(pady=5)
        new_entry = tk.Entry(frame, font=("Helvetica", 16))
        new_entry.pack(pady=5)
        self.create_button(frame, "Редактировать", lambda: self.edit_data(date_entry.get(), old_entry.get(), new_entry.get())).pack(pady=10)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

    def edit_data(self, date_str, old_entry, new_entry):
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        self.attendance_tracker.edit_attendance(date, old_entry, new_entry)
        messagebox.showinfo("Успех", "Данные успешно отредактированы.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_reading(self):
        import threading
        threading.Thread(target=self.rfid_reader.start_reading, daemon=True).start()

    def check_queue(self):
        try:
            while True:
                uid = self.callback_queue.get_nowait()
                self.update_label(uid)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)

    def update_label(self, uid):
        log_message = self.attendance_tracker.log_attendance(uid)
        if hasattr(self, 'label') and self.label.winfo_exists():
            self.label.config(text=log_message)

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, font=("Helvetica", 16), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", command=command)
        return button

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()