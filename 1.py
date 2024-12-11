import argparse
import os
import csv
import logging
import time
import psutil

# Set up logging
logging.basicConfig(filename='error_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_user(username, role):
    if role not in ['admin', 'user']:
        logging.error(f"Invalid role specified for user '{username}'.")
        return
    os.system(f'sudo useradd -m -s /bin/bash -G {role} {username}')
    logging.info(f"Creating user '{username}' with role '{role}'")
    logging.info(f"User  '{username}' created successfully with home directory /home/{username}")
    logging.info(f"Role '{role}' assigned with full access permissions.")

def create_batch_users(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            role = row['role']
            password = row['password']
            if role not in ['admin', 'user']:
                logging.error(f"Invalid role specified for user '{username}' in CSV file.")
                continue
            if os.system(f'id -u {username} > /dev/null 2>&1') == 0:
                logging.error(f"User  '{username}' already exists. Skipping.")
                continue
            create_user(username, role)
            os.system(f'echo "{username}:{password}" | sudo chpasswd')

def delete_user(username):
    os.system(f'sudo userdel -r {username}')
    logging.info(f"Deleting user '{username}'")
    logging.info(f"User  '{username}' deleted successfully.")

def update_user(username, password=None):
    if password:
        os.system(f'echo "{username}:{password}" | sudo chpasswd')
        logging.info(f"Updating information for user '{username}'")
        logging.info(f"Password updated successfully for '{username}'.")

def organize_files(directory):
    logging.info(f"Organizing files in {directory} by type")
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_extension = filename.split('.')[-1]
            target_dir = os.path.join(directory, f"{file_extension}_files")
            os.makedirs(target_dir, exist_ok=True)
            os.rename(os.path.join(directory, filename), os.path.join(target_dir, filename))
            logging.info(f"Moved .{file_extension} files to {target_dir}")
    logging.info("Directory organization complete.")

def monitor_logs(log_file):
    logging.info(f"Monitoring {log_file} for critical messages")
    with open(log_file, 'r') as file:
        for line in file:
            if "Error" in line:
                logging.warning(f"Critical message found: {line.strip()}")
                with open('error_summary.log', 'a') as summary_file:
                    summary_file.write(line)

def monitor_system():
    logging.info("System health check every 1 minute for 10 minutes")
    for _ in range(10):
        cpu_usage = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        logging.info(f"CPU Usage: {cpu_usage}% | Memory Usage: {memory_info.percent}%")
        if cpu_usage > 80:
            logging.warning(f"High CPU usage detected: {cpu_usage}%")
        time.sleep(60)

def check_disk_space(directory, threshold):
    disk_usage = psutil.disk_usage(directory)
    logging.info(f"Checking disk space for directory {directory}")
    if disk_usage.percent > threshold:
        logging.warning(f"Disk usage at {disk_usage.percent}% - consider freeing up space.")

def main():
    parser = argparse.ArgumentParser(description='System Administration Script')
    subparsers = parser.add_subparsers(dest='command')

    # User management commands
    user_parser = subparsers.add_parser('user')
    user_parser.add_argument('--create', action='store_true')
    user_parser.add_argument('--create-batch', action='store_true')
    user_parser.add_argument('--delete', action='store_true')
    user_parser.add_argument('--update', action='store_true')
    user_parser.add_argument('--username', type=str)
    user_parser.add_argument('--role', type=str)
    user_parser.add_argument('--csv', type=str)
    user_parser.add_argument('--password', type=str)

    # Organize files command
    organize_parser = subparsers.add_parser('organize')
    organize_parser.add_argument('--dir', type=str)
    organize_parser.add_argument('--log-monitor', type=str)

    # Monitor system command
    monitor_parser = subparsers.add_parser('monitor')
    monitor_parser.add_argument('--system', action='store_true')
    monitor_parser .add_argument('--disk', action='store_true')
    monitor_parser.add_argument('--dir', type=str)
    monitor_parser.add_argument('--threshold', type=int)

    args = parser.parse_args()

    if args.command == 'user':
        if args.create:
            create_user(args.username, args.role)
        elif args.create_batch:
            create_batch_users(args.csv)
        elif args.delete:
            delete_user(args.username)
        elif args.update:
            update_user(args.username, args.password)
    elif args.command == 'organize':
        if args.dir:
            organize_files(args.dir)
        elif args.log_monitor:
            monitor_logs(args.log_monitor)
    elif args.command == 'monitor':
        if args.system:
            monitor_system()
        elif args.disk and args.dir and args.threshold:
            check_disk_space(args.dir, args.threshold)

if __name__ == '__main__':
    main()
