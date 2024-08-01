import os
import re
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

log_file_path = os.getenv("LOG_FILE_PATH", "./logs/server.log")

log_pattern = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}), (?P<log_level>\w+): (?P<message>.*)')

def parse_log_line(log_line):
    try:
        match = log_pattern.match(log_line)
        return match.groupdict() if match else None
    except Exception as e:
        print(f"Error parsing log line: {log_line}. Error: {e}")
        return None

def detect_anomalies(log_entries):
    try:
        error_count = sum(log['log_level'] == 'ERROR' for log in log_entries)
        if error_count > 10:
            return True, f"High number of ERROR logs detected: {error_count}"
        return False, None
    except Exception as e:
        print(f"Error detecting anomalies: {e}")
        return False, None

def summarize_log_levels(log_entries):
    """
    Summarize occurrences of each log level in the provided log entries.
    """
    level_summary = {}
    for log in log_entries:
        try:
            if log['log_level'] in level_summary:
                level_summary[log['log_level']] += 1
            else:
                level_summary[log['log_level']] = 1
        except Exception as e:
            print(f"Error summarizing log levels: {log}. Error: {e}")
    return level_summary

def process_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            logs = file.readlines()
    except Exception as e:
        print(f"Error opening log file: {file_path}. Error: {e}")
        return None
    
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
    if report_data is not None:
        print(json.dumps(report_data, indent=4))
    else:
        print(json.dumps({"error": "Failed to generate report due to earlier errors."}, indent=4))

def main():
    report_data = process_log_file(log_file_path)
    generate_json(report_data)

if __name__ == "__main__":
    main()