def format_timestamp(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def calculate_time_difference(start_time, end_time):
    return (end_time - start_time).total_seconds() / 3600  # returns hours

def current_timestamp():
    from datetime import datetime
    return datetime.now()