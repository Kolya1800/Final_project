import argparse
import os
import logging
import shutil
import re

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='example.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

def organize_files(directory):
    logger.info(f"Organizing files in {directory} by type")
    if not os.path.exists(directory):
        logger.error(f"Directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        logger.info(f"Directory '{directory}' is empty. No files to organize.")
        return
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_extension = filename.split('.')[-1]
            target_dir = os.path.join(directory, f"{file_extension}_files")
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(os.path.join(directory, filename), os.path.join(target_dir, filename))
            logger.info(f"Moved .{file_extension} files to {target_dir}")
    logger.info("Directory organization complete.")

def monitor_log(log_file):
    logger.info(f"Monitoring log file {log_file}")
    if not os.path.exists(log_file):
        logger.error(f"Log file '{log_file}' does not exist.")
        return
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'error|warning|critical', line, re.IGNORECASE)
            if match:
                logger.warning(f"Found {match.group()} in log file: {line.strip()}")
    logger.info("Log file monitoring complete.")

def main():
    parser = argparse.ArgumentParser(description='File Organizer Script')
    subparsers = parser.add_subparsers(dest='command')

    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str, help='Directory to organize files in')

    monitor_parser = subparsers.add_parser('organize')
    monitor_parser.add_argument('--log-monitor', type=str, help='Log file to monitor')

    args = parser.parse_args()

    if args.command == 'organize':
        if args.dir:
            organize_files(args.dir)
        elif args.log_monitor:
            monitor_log(args.log_monitor)
        else:
            logger.error("Please specify a directory to organize files in or a log file to monitor.")

if __name__ == '__main__':
    main()
