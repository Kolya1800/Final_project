#!/usr/bin/python3
import argparse
import sys
import crypt
import pwd
import subprocess
import csv
import logging

# Set up logging
logging.basicConfig(
    filename="sys_admin.log", #change to your file name or make same one
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def user_exists(username) -> bool:
    try:
        pwd.getpwnam(username)
        logging.info(f"Checked existence of user '{username}': EXISTS.")
        return True
    except KeyError:
        logging.info(f"Checked existence of user '{username}': DOES NOT EXIST.")
        return False


def main():
    parser = argparse.ArgumentParser(
        prog="sys_admin",
        description="Manages system administration",
        add_help=True
    )
    parser.add_argument("option", type=str, choices=["user", "organization", "monitor"],
                        help="Choose option: [user, organization, monitor]")

    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser("create", help="Create new user")
    create_parser.add_argument("-u", "--username", type=str, action="store", help="Assign username")
    create_parser.add_argument("-p", "--password", type=str, action="store", help="Assign password")
    create_parser.add_argument("-r", "--role", type=str, action="store", help="Assign role: [user, admin]")

    batch_parser = subparsers.add_parser("create_batch", help="Create users from CSV")
    batch_parser.add_argument("-f", "--filename", type=str, action="store", help="Name of CSV file")

    delete_parser = subparsers.add_parser("delete", help="Delete existing user")
    delete_parser.add_argument("-u", "--username", type=str, action="store", help="Assign username")

    update_parser = subparsers.add_parser("update", help="Update existing user")
    update_parser.add_argument("-u", "--username", type=str, action="store", help="Current username")
    update_parser.add_argument("-n", "--new_username", type=str, action="store", default=None,
                               help="Assign new username")
    update_parser.add_argument("-p", "--password", type=str, action="store", default=None, help="Assign new password")
    update_parser.add_argument("-r", "--role", type=str, action="store", default=None,
                               help="Assign new role: [user, admin]")

    args = parser.parse_args()

    if args.option == "user":

        if "create" in args:
            if not args.username or not args.password or not args.role:
                print("You must include the username, password, and role.")
                sys.exit(1)
            else:
                create_user(args.username, args.password, args.role)

        if "create_batch" in args:
            if not args.filename:
                print("You must include the filename.")
            else:
                create_from_csv(args.filename)

        if "delete" in args:
            if not args.username:
                print("You must include the username.")
                sys.exit(1)
            else:
                deletes_user(args.username)

        if "update" in args:
            if not args.username or not args.newusername or not args.password or not args.role:
                print("You must include the username, password, and role.")
                sys.exit(1)
            else:
                modify_user(args.username, args.newusername, args.password, args.role)

    else:
        sys.exit(1)


def create_user(username: str, password: str, role: str):
    en_pwd = crypt.crypt(password)
    if user_exists(username):
        logging.warning(f"Cannot create user '{username}': Already exists.")
    try:
        subprocess.call(["useradd", "-p", en_pwd, username])
        logging.info(f"User '{username}' created successfully.")
        if role == "admin":
            subprocess.call(["usermod", "-g", "root", username])
            logging.info(f"Granted root access to user '{username}'.")
    except Exception as e:
        logging.error(f"Error creating user '{username}': {e}")


def create_user_two(username: str, role: str, password: str):
    if user_exists(username):
        logging.warning(f"User '{username}' exists. Skipping creation.")
    else:
        en_pwd = crypt.crypt(password)

        subprocess.call(["useradd", "-p", en_pwd, username])
        # if role == "admin":
        #     subprocess.call(["usermod", "-g", "root", username])

        try:
            subprocess.call(["useradd", "-p", en_pwd, username])
            logging.info(f"User '{username}' created successfully.")
            if role == "admin":
                subprocess.call(["usermod", "-g", "root", username])
            # if role.lower() == "admin":
            #     subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Granted admin privileges to user '{username}'.")
        except Exception as e:
            logging.error(f"Error creating user '{username}': {e}")


def create_from_csv(filename):
    """Create users in batch from a CSV file."""
    try:
        with open(filename, "r") as fPtr:
            reader = csv.reader(fPtr)
            next(reader)  # Skip header row
            for row in reader:
                create_user_two(row[0], row[1], row[2])
        logging.info(f"Batch creation from '{filename}' completed successfully.")
    except FileNotFoundError:
        logging.error(f"CSV file '{filename}' not found.")
    except Exception as e:
        logging.error(f"Error creating users from CSV file '{filename}': {e}")


def deletes_user(username: str):
    if user_exists(username):
        try:
            subprocess.call(["userdel", "-r", username])
            logging.info(f"User '{username}' deleted successfully.")
        except Exception as e:
            logging.error(f"Failed to delete user '{username}': {e}")
    else:
        logging.warning(f"Cannot delete user '{username}': Does not exist.")


def modify_user(old_username: str, new_username: str, new_password: str, new_role: str):
    # if new_username is not None:
    #     subprocess.call(["usermod", "-l", new_username, old_username])
    #     if new_password is not None:
    #         subprocess.call(["usermod", "-p", new_password, new_username])
    #     if new_role is not None:
    #         subprocess.call(["usermod", "-g", "root", new_username])
    #
    # else:
    #     if new_password is not None:
    #         subprocess.call(["usermod", "-p", new_password, old_username])
    #     if new_role is not None:
    #         subprocess.call(["usermod", "-g", "root", old_username])
    if user_exists(old_username):
        if new_role == "admin":
            subprocess.call(["usermod", "-g", "root", old_username])
        if new_role == "user":
            subprocess.call(["deluser", old_username, "sudo"])
        if new_password is not None:
            subprocess.call(["usermod", "-p", new_password, old_username])
        if new_username is not None:
            subprocess.call(["usermod", "-l", new_username, old_username])


if __name__ == '__main__':
    main()
