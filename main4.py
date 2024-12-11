import argparse
import os
import psutil
import time
import logging
import shutil
import re

# Set up logging
logging.basicConfig(
    filename='system_health.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def organize_files(directory):
    logging.info(f"Organizing files in {directory} by type")
    if not os.path.exists(directory):
        logging.error(f"Directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        logging.info(f"Directory '{directory}' is empty. No files to organize.")
        return
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_extension = filename.split('.')[-1]
            target_dir = os.path.join(directory, f"{file_extension}_files")
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(os.path.join(directory, filename), os.path.join(target_dir, filename))
            logging.info(f"Moved .{file_extension} files to {target_dir}")
    logging.info("Directory organization complete.")

def monitor_log(log_file):
    logging.info(f"Monitoring {log_file} for critical messages")
    if not os.path.exists(log_file):
        logging.error(f"Log file '{log_file}' does not exist.")
        return
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'critical', line, re.IGNORECASE)
            if match:
                logging.warning(f"Critical message found: {line.strip()}")
    logging.info("Logged critical messages to error_summary.log.")

def monitor_system():
    logging.info("System health check every 1 minute for 10 minutes")
    for _ in range(10):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        logging.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}%")
        if cpu_usage > 80:
            logging.warning(f"High CPU usage detected: {cpu_usage}%")
        time.sleep(60)
    logging.info("Logged CPU and memory usage to system_health.log.")

def check_disk_space(directory, threshold):
    disk_usage = psutil.disk_usage(directory)
    logging.info(f"Checking disk space for directory {directory}")
    if disk_usage.percent > threshold:
        logging.warning(f"Disk usage at {disk_usage.percent}% - consider freeing up space.")

def list_processes(process_name=None):
    processes = [p.info for p in psutil.process_iter(['pid', 'name'])]
    if process_name:
        processes = [p for p in processes if p['name'] == process_name]
    return processes

def main():
    parser = argparse.ArgumentParser(description='System Administration Script')
    subparsers = parser.add_subparsers(dest='command')

    # Organize files command
    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str, help='Directory to organize files in')
    organize_parser.add_argument('--log-monitor', type=str, help='Log file to monitor')

    # Monitor system command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--system', action='store_true')
    monitor_parser.add_argument('--disk', action='store_true')
    monitor_parser.add_argument('--threshold', type=int)


    args = parser.parse_args()

    if args.command == 'organize':
        if args.dir:
            organize_files(args.dir)
        elif args.log_monitor:
            monitor_log(args.log_monitor)
        else:
            logging.error("Please specify a directory to organize files in or a log file to monitor.")
    elif args.command == 'monitor':
        if args.system:
            monitor_system()
        elif args.disk and args.dir and args.threshold:
            check_disk_space(args.dir, args.threshold)
        elif args.process:
            processes = list_processes(args.process)
            for process in processes:
                logging.info(f"Process ID: {process['pid']} | Process Name: {process['name']}")
        else:
            logging.error("Please specify a valid monitoring option.")
    else:
        logging.error("Please specify a command (organize or monitor).")

if __name__ == '__main__':
    main()
