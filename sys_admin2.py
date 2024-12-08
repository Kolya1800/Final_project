import os
import shutil
import argparse
import logging
import psutil
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def organize_files(directory):
    logging.info(f'Organizing files in {directory} by type')
    
    file_types = {
        'text_files': ['.txt'],
        'log_files': ['.log'],
        'image_files': ['.jpg', '.jpeg', '.png'],
        'pdf_files': ['.pdf'],
    }

    for folder, extensions in file_types.items():
        folder_path = os.path.join(directory, folder)
        os.makedirs(folder_path, exist_ok=True)

        for filename in os.listdir(directory):
            if any(filename.endswith(ext) for ext in extensions):
                src_path = os.path.join(directory, filename)
                dest_path = os.path.join(folder_path, filename)
                shutil.move(src_path, dest_path)
                logging.info(f'Moved {filename} to {folder_path}')

    logging.info('Directory organization complete.')

def monitor_system():
    logging.info('System health check every 1 minute for 10 minutes')
    with open('system_health.log', 'w') as log_file:
        for _ in range(10):
            cpu_usage = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            log_file.write(f'CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%\n')
            logging.info(f'CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%')
            if cpu_usage > 80:
                logging.warning(f'High CPU usage detected: {cpu_usage}%')
            time.sleep(60)

def check_disk_space(directory, threshold):
    logging.info(f'Checking disk space for directory {directory}')
    disk_usage = psutil.disk_usage(directory)
    usage_percent = disk_usage.percent
    if usage_percent > threshold:
        logging.warning(f'Disk usage at {usage_percent}% - consider freeing up space.')

def list_processes(name_filter=None):
    logging.info('Listing processes')
    for proc in psutil.process_iter(['pid', 'name']):
        if name_filter is None or name_filter in proc.info['name']:
            logging.info(f'Process ID: {proc.info["pid"]}, Name: {proc.info["name"]}')

def main():
    parser = argparse.ArgumentParser(description='System Administration Script')
    subparsers = parser.add_subparsers(dest='command')

    # Directory organization command
    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str, help='Directory to organize')
    organize_parser.add_argument('--log-monitor', type=str, help='Log file to monitor')

    # System health monitoring command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--system', action='store_true', help='Monitor CPU and memory usage')
    monitor_parser.add_argument('--disk', action='store_true', help='Check disk space')
    monitor_parser.add_argument('--dir', type=str, help='Directory to check disk space')
    monitor_parser.add_argument('--threshold', type=int, help='Disk usage threshold percentage')

    args = parser.parse_args()

    if args.command == 'organize':
        if args.dir:
            organize_files(args.dir)
        if args.log_monitor:
            monitor_logs(args.log_monitor)

    elif args.command == 'monitor':
        if args.system:
            monitor_system()
        if args.disk and args.dir and args.threshold is not None:
            check_disk_space(args.dir, args.threshold)
        if args.disk and not args.dir:
            logging.error('Directory must be specified for disk space check.')

if __name__ == '__main__':
    main()