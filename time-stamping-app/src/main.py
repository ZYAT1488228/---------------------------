import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import queue
from rfid_reader import RfidReader
from attendance_tracker import AttendanceTracker
import datetime
import logging
from pynput import keyboard

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    def __init__(self, root):
    
        self.root = root
        self.root.title("RFID Attendance Tracker")
        self.root.geometry("600x400")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 16), background="#2c3e50", foreground="white")
        self.style.configure("TFrame", background="#2c3e50")

        self.attendance_tracker = AttendanceTracker()
        self.callback_queue = queue.Queue()
        self.rfid_reader = RfidReader(self.callback_queue)
        self.input_buffer = ""

        self.main_menu()
        self.start_reading()
        self.check_queue()

        # Start keyboard listener
        self.start_keyboard_listener()

        logging.debug("Приложение инициализировано")

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    self.input_buffer += key.char
                    if len(self.input_buffer) >= 10:  # Предполагаем, что UID состоит из 10 символов
                        self.callback_queue.put(self.input_buffer)
                        self.input_buffer = ""
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def reset_focus_and_clear_input(self, event=None):
        logging.debug("Сброс фокуса и очистка ввода")
        self.root.focus_set()

    def reset_focus(self, event=None):
        logging.debug("Сброс фокуса")
        self.root.focus_set()

    def main_menu(self):
        logging.debug("Переход в главное меню")
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="RFID Attendance Tracker", font=("Helvetica", 20)).pack(pady=20)
        self.create_button(frame, "Регистрация времени", self.registration_screen).pack(pady=10)
        self.create_button(frame, "Просмотр данных", self.view_data_screen).pack(pady=10)
        self.create_button(frame, "Подсчет времени", self.calculate_hours_screen).pack(pady=10)
        self.create_button(frame, "Редактирование данных", self.edit_data_screen).pack(pady=10)

        self.reset_focus_and_clear_input()

    def registration_screen(self):
        logging.debug("Переход на экран регистрации времени")
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        self.label = ttk.Label(frame, text="Приложите RFID-карту для регистрации времени...")
        self.label.pack(pady=20)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

        self.reset_focus_and_clear_input()

    def view_data_screen(self):
        logging.debug("Переход на экран просмотра данных")
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Выберите дату для просмотра данных", font=("Helvetica", 20)).pack(pady=20)
        date_entry = tk.Entry(frame, font=("Helvetica", 16))
        date_entry.pack(pady=10)
        self.create_button(frame, "Показать данные", lambda: self.show_data(date_entry.get())).pack(pady=10)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

        self.reset_focus_and_clear_input()

    def show_data(self, date_str):
        logging.debug(f"Показ данных за дату: {date_str}")
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

        self.reset_focus_and_clear_input()

    def calculate_hours_screen(self):
        logging.debug("Переход на экран подсчета времени")
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(frame, text="Введите месяц для подсчета времени (ГГГГ-ММ)", font=("Helvetica", 20)).pack(pady=20)
        month_entry = tk.Entry(frame, font=("Helvetica", 16))
        month_entry.pack(pady=10)
        self.create_button(frame, "Показать данные", lambda: self.show_hours(month_entry.get())).pack(pady=10)
        self.create_button(frame, "Назад", self.main_menu).pack(pady=10)

        self.reset_focus_and_clear_input()

    def show_hours(self, month_str):
        logging.debug(f"Показ отработанных часов за месяц: {month_str}")
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

        self.reset_focus_and_clear_input()

    def edit_data_screen(self):
        logging.debug("Переход на экран редактирования данных")
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

        self.reset_focus_and_clear_input()

    def edit_data(self, date_str, old_entry, new_entry):
        logging.debug(f"Редактирование данных за дату: {date_str}")
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return

        self.attendance_tracker.edit_attendance(date, old_entry, new_entry)
        messagebox.showinfo("Успех", "Данные успешно отредактированы.")

        self.reset_focus_and_clear_input()

    def clear_window(self):
        logging.debug("Очистка окна")
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_reading(self):
        logging.debug("Запуск чтения RFID")
        import threading
        threading.Thread(target=self.rfid_reader.start_reading, daemon=True).start()
        logging.debug("Поток чтения RFID запущен")

    def check_queue(self):
        try:
            while True:
                uid = self.callback_queue.get_nowait()
                logging.debug(f"UID получен: {uid}")
                self.update_label(uid)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)

    def update_label(self, uid):
        logging.debug(f"Обновление метки для UID: {uid}")
        log_message = self.attendance_tracker.log_attendance(uid)
        if log_message:
            if hasattr(self, 'label') and self.label.winfo_exists():
                self.label.config(text=log_message)
            else:
                print(log_message)
            logging.debug(f"Логирование метки: {log_message}")
        else:
            logging.debug(f"UID {uid} не распознан, запись пропущена.")

    def create_button(self, parent, text, command):
        button = tk.Button(parent, text=text, font=("Helvetica", 16), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", command=command)
        return button

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()