import argparse
import os.path
import csv
import subprocess
import logging

# Set up logging
logging.basicConfig(filename='sys_admin.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_user(username, role):
    try:
        if role not in ['admin', 'user']:
            raise ValueError(f"Invalid role specified for user '{username}'")

        # Check if the user already exists
        if user_exists(username):
            logging.error(f"User '{username}' already exists.")
            return f"[ERROR] User '{username}' already exists."

        # Create user with the specified role
        subprocess.run(['sudo', 'useradd', '-m', '-d', f'/home/{username}', '-s', '/bin/bash', username], check=True)
        set_permissions(username, role)

        logging.info(f"User '{username}' created successfully with home directory /home/{username}")
        return f"[INFO] User '{username}' created successfully with home directory /home/{username}"

    except ValueError as e:
        logging.error(str(e))
        return f"[ERROR] {str(e)}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating user '{username}': {e}")
        return f"[ERROR] Error creating user '{username}'"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"[ERROR] Unexpected error: {e}"

def create_multiple_users_from_csv(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['username']
                role = row['role']
                password = row['password']

                if role not in ['admin', 'user']:
                    logging.error(f"Invalid role specified for user '{username}' in CSV file.")
                    continue

                if user_exists(username):
                    logging.error(f"User '{username}' already exists. Skipping.")
                    continue

                # Create user and assign role
                create_user(username, role)
                set_user_password(username, password)

        logging.info("Batch user creation completed successfully.")
        return "[INFO] Batch user creation completed successfully."

    except FileNotFoundError as e:
        logging.error(f"CSV file not found: {csv_file}")
        return f"[ERROR] CSV file not found: {csv_file}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"[ERROR] Unexpected error: {e}"

def delete_user(username):
    try:
        if not user_exists(username):
            logging.error(f"User '{username}' does not exist.")
            return f"[ERROR] User '{username}' does not exist."

        subprocess.run(['sudo', 'userdel', '-r', username], check=True)
        logging.info(f"User '{username}' deleted successfully.")
        return f"[INFO] User '{username}' deleted successfully."

    except subprocess.CalledProcessError as e:
        logging.error(f"Error deleting user '{username}': {e}")
        return f"[ERROR] Error deleting user '{username}'"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"[ERROR] Unexpected error: {e}"

def update_user(username, password=None):
    try:
        if not user_exists(username):
            logging.error(f"User '{username}' not found.")
            return f"[ERROR] User '{username}' not found."

        if password:
            set_user_password(username, password)
        
        logging.info(f"Password updated successfully for '{username}'.")
        return f"[INFO] Password updated successfully for '{username}'."

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"[ERROR] Unexpected error: {e}"

def user_exists(username):
    result = subprocess.run(['id', username], capture_output=True)
    return result.returncode == 0

def set_permissions(username, role):
    # Assign permissions based on the role
    if role == 'admin':
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', username], check=True)
        logging.info(f"Role 'admin' assigned with full access permissions for user '{username}'")
    else:
        logging.info(f"Role 'user' assigned with basic access for user '{username}'")

def set_user_password(username, password):
    subprocess.run(['sudo', 'chpasswd'], input=f"{username}:{password}".encode(), check=True)
    logging.info(f"Password set for user '{username}'")

def display_help():
    help_text = """
    Usage: python3 sys_admin.py user [options]
    Options:
    --create        Create a single user (requires --username and --role).
    --create-batch  Create multiple users from a CSV file (requires --csv).
    --delete        Delete a user (requires --username).
    --update        Update user details (requires --username, optional --password).
    """
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description='System Administration Tool')
    subparsers = parser.add_subparsers(dest='command')

    # User management subcommands
    user_parser = subparsers.add_parser('user', help='User management')
    user_subparsers = user_parser.add_subparsers(dest='user_command')

    # Create user
    user_subparsers.add_parser('create', help='Create a single user')
    user_subparsers.add_parser('create-batch', help='Create users from CSV')
    user_subparsers.add_parser('delete', help='Delete a user')
    user_subparsers.add_parser('update', help='Update user details')

    args = parser.parse_args()

    if args.command == 'user':
        if args.user_command == 'create':
            print(create_user(args.username, args.role))
        elif args.user_command == 'create-batch':
            print(create_multiple_users_from_csv(args.csv))
        elif args.user_command == 'delete':
            print(delete_user(args.username))
        elif args.user_command == 'update':
            print(update_user(args.username, args.password))
        else:
            display_help()

if __name__ == "__main__":
    main()
