import os
from datetime import date

def init_logging_file():
    folder_logs = "logs"
    num_files = len(os.listdir(folder_logs))
    return f"{folder_logs}/log_{num_files+1}_{date.today()}.txt"

def get_lastest_logs():
    folder_logs = "logs"
    num_files = len(os.listdir(folder_logs))
    result = ""
    for fname in os.listdir(folder_logs):
        if f"_{num_files}_" in fname:
            result = fname
            break
    return f"{folder_logs}/{result}"