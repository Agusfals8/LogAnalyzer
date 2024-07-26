import os
import re
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

log_file_path = os.getenv("LOG_FILE_PATH", "./logs/server.log")

log_pattern = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (?P<log_level>\w+): (?P<message>.*)')

def extract_metrics_from_log(log_line):
    match = log_pattern.match(log_line)
    if match:
        return match.groupdict()
    return None

def identify_anomalies(log_data):
    error_count = sum(1 for log in log_data if log['log_level'] == 'ERROR')
    if error_count > 10:
        return True, f"High number of ERROR logs detected: {error_count}"
    return False, None

def process_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    
    extracted_logs = [extract_metrics_from_log(log) for log in logs if extract_time_from_log(log)]
    anomalies_found, anomaly_message = identify_anomalies(extracted_logs)
    
    report = {
        "total_logs": len(logs),
        "anomalies_found": anomalies_found,
        "anomaly_message": anomaly_message
    }
    return report

def extract_time_from_log(log_line):
    match = log_pattern.match(log_log_line)
    if match:
        log_time = datetime.strptime(match.group('date'), "%Y-%m-%d %H:%M:%S")
        return log_time
    return None

def generate_report(report_data):
    print(json.dumps(report_data, indent=4))

def main():
    report_data = process_log_file(log_file_path)
    generate_report(report_data)

if __name__ == "__main__":
    main()