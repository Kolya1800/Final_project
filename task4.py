import argparse
import os
import psutil
import time
import logging

# Set up logging
logging.basicConfig(filename='system_health.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    # Monitor system command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--system', action='store_true')
    monitor_parser.add_argument('--disk', action='store_true')
    monitor_parser.add_argument('--dir', type=str)
    monitor_parser.add_argument('--threshold', type=int)
    monitor_parser.add_argument('--process', type=str)

    args = parser.parse_args()

    if args.command == 'monitor':
        if args.system:
            monitor_system()
        elif args.disk and args.dir and args.threshold:
            check_disk_space(args.dir, args.threshold)
        elif args.process:
            processes = list_processes(args.process)
            for process in processes:
                logging.info(f"Process ID: {process['pid']} | Process Name: {process['name']}")

if __name__ == '__main__':
    main()