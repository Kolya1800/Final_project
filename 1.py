#!/usr/bin/python
import os
import shutil
import argparse
import logging
import crypt
import csv
import getpass
import psutil
import time


# Set up centralized logging
logging.basicConfig(
    filename="sys_admin.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -----------------------------
# User Management Functions
# -----------------------------

def user_exists(username) -> bool:
    """Check if a user exists on the system."""
    try:
        return username in [entry.pw_name for entry in os.scandir('/etc/passwd')]
    except Exception as e:
        logging.error(f"Error checking user existence: {e}")
        return False


def create_user(username, role, password=None):
    """Create a single user with the specified role and password."""
    if user_exists(username):
        logging.error(f"User '{username}' already exists.")
        return

    try:
        encrypted_password = crypt.crypt(password or "defaultpass123")
        os.system(f"useradd -m -p {encrypted_password} {username}")
        if role == "admin":
            os.system(f"usermod -aG sudo {username}")
        logging.info(f"User '{username}' created with role '{role}'.")
    except Exception as e:
        logging.error(f"Failed to create user '{username}': {e}")


def delete_user(username):
    """Delete a user from the system."""
    if not user_exists(username):
        logging.error(f"User '{username}' does not exist.")
        return

    try:
        os.system(f"userdel -r {username}")
        logging.info(f"User '{username}' deleted successfully.")
    except Exception as e:
        logging.error(f"Failed to delete user '{username}': {e}")


def update_user(username, password=None):
    """Update user details such as password."""
    if not user_exists(username):
        logging.error(f"User '{username}' does not exist.")
        return

    try:
        if password:
            encrypted_password = crypt.crypt(password)
            os.system(f"usermod -p {encrypted_password} {username}")
        logging.info(f"User '{username}' updated successfully.")
    except Exception as e:
        logging.error(f"Failed to update user '{username}': {e}")


def create_users_from_csv(csv_file):
    """Create multiple users from a CSV file."""
    try:
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                username, role, password = row["username"], row["role"], row["password"]
                if role not in ["admin", "user"]:
                    logging.error(f"Invalid role '{role}' for user '{username}'. Skipping.")
                    continue
                create_user(username, role, password)
        logging.info("Batch user creation completed successfully.")
    except FileNotFoundError:
        logging.error(f"CSV file '{csv_file}' not found.")
    except Exception as e:
        logging.error(f"Error creating users from CSV: {e}")


# -----------------------------
# File Organization Functions
# -----------------------------

def organize_files(directory):
    """Organize files in a directory based on their type."""
    logging.info(f"Organizing files in {directory} by type.")
    file_types = {
        "text_files": [".txt"],
        "log_files": [".log"],
        "image_files": [".jpg", ".jpeg", ".png"],
        "pdf_files": [".pdf"],
    }

    try:
        for folder, extensions in file_types.items():
            folder_path = os.path.join(directory, folder)
            os.makedirs(folder_path, exist_ok=True)

            for filename in os.listdir(directory):
                if any(filename.endswith(ext) for ext in extensions):
                    src_path = os.path.join(directory, filename)
                    dest_path = os.path.join(folder_path, filename)
                    shutil.move(src_path, dest_path)
                    logging.info(f"Moved {filename} to {folder_path}.")
        logging.info("Directory organization complete.")
    except Exception as e:
        logging.error(f"Error organizing files: {e}")


def monitor_logs(log_file):
    """Monitor a log file for critical messages."""
    logging.info(f"Monitoring log file: {log_file}.")
    try:
        with open(log_file, "r") as file:
            for line in file:
                if "critical" in line.lower():
                    logging.warning(f"Critical message found: {line.strip()}")
    except FileNotFoundError:
        logging.error(f"Log file '{log_file}' not found.")
    except Exception as e:
        logging.error(f"Error monitoring log file '{log_file}': {e}")


# -----------------------------
# System Monitoring Functions
# -----------------------------

def monitor_system():
    """Monitor system health."""
    logging.info("Starting system health monitoring for 10 minutes.")
    try:
        with open("system_health.log", "w") as log_file:
            for _ in range(10):
                cpu_usage = psutil.cpu_percent()
                memory_info = psutil.virtual_memory().percent
                log_file.write(f"CPU: {cpu_usage}%, Memory: {memory_info}%\n")
                logging.info(f"CPU: {cpu_usage}%, Memory: {memory_info}%")
                if cpu_usage > 80:
                    logging.warning(f"High CPU usage: {cpu_usage}%")
                time.sleep(60)
    except Exception as e:
        logging.error(f"Error during system health monitoring: {e}")


def check_disk_space(directory, threshold):
    """Check disk space usage for a directory."""
    logging.info(f"Checking disk space for {directory}.")
    try:
        usage = psutil.disk_usage(directory).percent
        if usage > threshold:
            logging.warning(f"Disk usage at {usage}%. Free up space.")
    except FileNotFoundError:
        logging.error(f"Directory '{directory}' not found.")
    except Exception as e:
        logging.error(f"Error checking disk space: {e}")


# -----------------------------
# Main Command-Line Interface
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="System Administration Script")
    subparsers = parser.add_subparsers(dest="command")

    # User Management Commands
    user_parser = subparsers.add_parser("user", help="User management")
    user_parser.add_argument("--create", action="store_true", help="Create a single user")
    user_parser.add_argument("--create-batch", help="Create users from a CSV file")
    user_parser.add_argument("--delete", action="store_true", help="Delete a user")
    user_parser.add_argument("--update", action="store_true", help="Update a user")
    user_parser.add_argument("--username", help="Username of the user")
    user_parser.add_argument("--role", help="Role of the user (admin/user)")
    user_parser.add_argument("--password", help="Password for the user")

    # File Organization Commands
    organize_parser = subparsers.add_parser("organize", help="Organize files and monitor logs")
    organize_parser.add_argument("--dir", help="Directory to organize files")
    organize_parser.add_argument("--log-monitor", help="Log file to monitor for critical messages")

    # System Monitoring Commands
    monitor_parser = subparsers.add_parser("monitor", help="Monitor system health")
    monitor_parser.add_argument("--system", action="store_true", help="Monitor CPU and memory")
    monitor_parser.add_argument("--disk", action="store_true", help="Check disk space")
    monitor_parser.add_argument("--dir", help="Directory to check disk space")
    monitor_parser.add_argument("--threshold", type=int, help="Disk space usage threshold")

    args = parser.parse_args()

    # Handle User Management
    if args.command == "user":
        if args.create:
            create_user(args.username, args.role, args.password)
        elif args.create_batch:
            create_users_from_csv(args.create_batch)
        elif args.delete:
            delete_user(args.username)
        elif args.update:
            update_user(args.username, args.password)

    # Handle File Organization
    elif args.command == "organize":
        if args.dir:
            organize_files(args.dir)
        if args.log_monitor:
            monitor_logs(args.log_monitor)

    # Handle System Monitoring
    elif args.command == "monitor":
        if args.system:
            monitor_system()
        if args.disk and args.dir and args.threshold:
            check_disk_space(args.dir, args.threshold)

if __name__ == "__main__":
    main()
