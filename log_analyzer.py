import os
import re
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

log_file_path = os.getenv("LOG_FILE_PATH", "./logs/server.log")

log_pattern = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (?P<log_level>\w+): (?P<message>.*)')

def parse_log_line(log_line):
    match = log_pattern.match(log_line)
    return match.groupdict() if match else None

def detect_anomalies(log_entries):
    error_count = sum(log['log_level'] == 'ERROR' for log in log_entries)
    if error_count > 10:
        return True, f"High number of ERROR logs detected: {error_count}"
    return False, None

def process_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    
    parsed_logs = [parse_log_line(log) for log in logs if parse_log_line(log)]
    
    anomalies_found, anomaly_message = detect_anomalies(parsed_logs)
    
    report = {
        "total_logs": len(logs),
        "anomalies_found": anomalies_found,
        "anomaly_message": anomaly_message
    }
    return report

def generate_report(report_data):
    print(json.dumps(report_data, indent=4))

def main():
    report_data = process_log_file(log_file_path)
    generate_json(report_data)

if __name__ == "__main__":
    main()