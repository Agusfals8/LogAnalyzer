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

def summarize_log_levels(log_entries):
    """
    Summarize occurrences of each log level in the provided log entries.
    """
    level_summary = {}
    for log in log_entries:
        if log['log_level'] in level_summary:
            level_summary[log['log_level']] += 1
        else:
            level_summary[log['log_level']] = 1
    return level_summary

def process_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    
    parsed_logs = [parse_log_line(log) for log in logs if parse_log_line(log)]
    
    anomalies_found, anomaly_message = detect_anomalies(parsed_logs)
    log_levels_summary = summarize_log_levels(parsed_logs)
    
    report = {
        "total_logs": len(logs),
        "parsed_logs": len(parsed_logs),
        "anomalies_found": anomalies_found,
        "anomaly_message": anomaly_message,
        "log_levels_summary": log_levels_summary
    }
    return report

def generate_json(report_data):
    print(json.dumps(report_data, indent=4))

def main():
    report_data = process_log_file(log_file_path)
    generate_json(report_data)

if __name__ == "__main__":
    main()