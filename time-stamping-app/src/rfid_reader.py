import re
import queue

class RfidReader:
    def __init__(self, callback_queue):
        self.callback_queue = callback_queue
        self.buffer = ""

    def start_reading(self):
        import keyboard
        print("🎯 RFID ридер готов. Приложите карту...")

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.handle_card_data(event.name)

    def handle_card_data(self, key):
        if key == "enter":
            uid = self.extract_uid(self.buffer)
            self.buffer = ""
            if uid:
                print(f"Карта приложена: {uid}")
                self.callback_queue.put(uid)
        elif key == "backspace":
            self.buffer = self.buffer[:-1]
        elif len(key) == 1:
            self.buffer += key

    def extract_uid(self, data):
        # Регулярное выражение для поиска UID
        match = re.search(r'\b[A-Z0-9]{10}\b', data)
        if match:
            return match.group(0)
        return None