# Time-Stamping Application

This project is a time-stamping application designed to track employee attendance using an RFID card reader. It records when employees arrive and leave, and calculates their working hours.

## Project Structure

```
time-stamping-app
├── src
│   ├── main.py               # Entry point of the application
│   ├── rfid_reader.py        # Manages interaction with the RFID card reader
│   ├── attendance_tracker.py  # Tracks employee attendance
│   └── utils
│       └── time_utils.py     # Utility functions for time-related operations
├── requirements.txt          # Lists project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd time-stamping-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Connect the RFID card reader to your computer.
2. Run the application:
   ```
   python src/main.py
   ```
3. Present your RFID card to record attendance.

## Features

- Records arrival and departure times.
- Calculates total working hours.
- Supports multiple employees through unique RFID cards.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.