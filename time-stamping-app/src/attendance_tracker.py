import datetime
import os
import json

class AttendanceTracker:
    def __init__(self):
        self.uid_to_name = {
            "0285212673": "Максим Бармен",
            "0285212674": "Максим Официант",
            "0285212675": "Катя",
            "0285212677": "Серафима",
            "0285212707": "Ева",
            "0285212708": "София",
            "0285212709": "Алина",
            "0285212710": "Люба",
            "0285212711": "Вовичк"
        }
        self.log_directory = "attendance_logs"
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def log_attendance(self, uid):
        current_time = datetime.datetime.now()
        name = self.uid_to_name.get(uid, "Неизвестный")
        status = "пришел" if self.is_odd_entry(uid) else "ушел"
        log_message = f"{name} (UID: {uid}) {status} в {current_time}"
        self.write_to_file(uid, name, current_time, status)
        return log_message

    def is_odd_entry(self, uid):
        count = 0
        for filename in os.listdir(self.log_directory):
            with open(os.path.join(self.log_directory, filename), "r", encoding="utf-8") as file:
                for line in file:
                    if f"(UID: {uid})" in line:
                        count += 1
        return count % 2 == 0

    def write_to_file(self, uid, name, current_time, status):
        date_str = current_time.strftime("%Y-%m-%d")
        filename = os.path.join(self.log_directory, f"{date_str}.txt")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{current_time} - {name} (UID: {uid}) {status}\n")

    def get_attendance(self, date):
        date_str = date.strftime("%Y-%m-%d")
        filename = os.path.join(self.log_directory, f"{date_str}.txt")
        if not os.path.exists(filename):
            return []
        with open(filename, "r", encoding="utf-8") as file:
            return file.readlines()

    def calculate_hours(self, month):
        attendance_log = {uid: [] for uid in self.uid_to_name.keys()}
        for filename in os.listdir(self.log_directory):
            if filename.startswith(month):
                with open(os.path.join(self.log_directory, filename), "r", encoding="utf-8") as file:
                    for line in file:
                        parts = line.strip().split(" - ")
                        if len(parts) == 2:
                            timestamp, info = parts
                            uid = info.split(" (UID: ")[1].split(")")[0]
                            if uid in self.uid_to_name:
                                time = datetime.datetime.fromisoformat(timestamp)
                                attendance_log[uid].append(time)
        hours_worked = {}
        for uid, times in attendance_log.items():
            total_seconds = 0
            for i in range(0, len(times), 2):
                if i + 1 < len(times):
                    total_seconds += (times[i + 1] - times[i]).total_seconds()
            hours_worked[uid] = total_seconds / 3600  # Convert seconds to hours
        return hours_worked

    def edit_attendance(self, date, old_entry, new_entry):
        date_str = date.strftime("%Y-%m-%d")
        filename = os.path.join(self.log_directory, f"{date_str}.txt")
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open(filename, "w", encoding="utf-8") as file:
            for line in lines:
                if line.strip() == old_entry.strip():
                    file.write(new_entry + "\n")
                else:
                    file.write(line)