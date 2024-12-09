#!/usr/bin/python
import crypt
import csv
import getpass
import pwd
import subprocess
import sys
import logging

# Setup logging
logging.basicConfig(
    filename="mai.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def user_exists(username) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def create_user(username: str):
    password = getpass.getpass(f"Enter the password for this user '{username}': ")
    role = input(f"Give user '{username}' root access (y/n)? ")
    en_pwd = crypt.crypt(password)

    if user_exists(username):
        logging.warning(f"The user '{username}' already exists. Skipping creation.")
    else:
        try:
            subprocess.call(["useradd", "-p", en_pwd, username])
            logging.info(f"User '{username}' created successfully.")
        except Exception as e:
            logging.error(f"Failed to create user '{username}': {e}")
    if role.lower() == "y":
        try:
            subprocess.call(["usermod", "-aG", "root", username])
            logging.info(f"Admin privileges granted to user '{username}'.")
        except Exception as e:
            logging.error(f"Failed to assign admin privileges to user '{username}': {e}")


def modify_user(username):
    print("1. Change password")
    print("2. Change role")
    print("3. Change both")
    mod_option = -1
    while mod_option not in [1, 2, 3]:
        mod_option = int(input("Select a valid option [1,2,3]: "))

    if mod_option == 1:
        new_pass = getpass.getpass(f"Enter the new password for user '{username}': ")
        en_newpass = crypt.crypt(new_pass)
        try:
            subprocess.call(["usermod", "-p", en_newpass, username])
            logging.info(f"Password updated successfully for user '{username}'.")
        except Exception as e:
            logging.error(f"Failed to update password for user '{username}': {e}")

    if mod_option == 2:
        new_role = input(f"Give user '{username}' root access (y/n)? ")
        if new_role.lower() == "y":
            try:
                subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Admin privileges granted to user '{username}'.")
            except Exception as e:
                logging.error(f"Failed to assign admin privileges to user '{username}': {e}")

    if mod_option == 3:
        new_pass = getpass.getpass(f"Enter the new password for user '{username}': ")
        en_newpass = crypt.crypt(new_pass)
        try:
            subprocess.call(["usermod", "-p", en_newpass, username])
            logging.info(f"Password updated successfully for user '{username}'.")
        except Exception as e:
            logging.error(f"Failed to update password for user '{username}': {e}")

        new_role = input(f"Give user '{username}' root access (y/n)? ")
        if new_role.lower() == "y":
            try:
                subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Admin privileges granted to user '{username}'.")
            except Exception as e:
                logging.error(f"Failed to assign admin privileges to user '{username}': {e}")


def create_user_two(username, role, password):
    if user_exists(username):
        logging.warning(f"User '{username}' already exists. Skipping creation.")
    else:
        en_pwd = crypt.crypt(password)
        try:
            subprocess.call(["useradd", "-p", en_pwd, username])
            logging.info(f"User '{username}' created successfully.")
            if role == "admin":
                subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Admin privileges granted to user '{username}'.")
        except Exception as e:
            logging.error(f"Failed to create user '{username}': {e}")


def deletes_user(username):
    if user_exists(username):
        try:
            subprocess.call(["userdel", "-r", username])
            logging.info(f"User '{username}' deleted successfully.")
        except Exception as e:
            logging.error(f"Failed to delete user '{username}': {e}")
    else:
        logging.warning(f"User '{username}' does not exist. Skipping deletion.")


def get_option():
    print("1. Create User")
    print("2. Remove existing user")
    print("3. Create users from CSV file")
    print("4. Modify existing user")
    print("5. Exit Program")
    select_option = -1
    while select_option not in [1, 2, 3, 4, 5]:
        select_option = int(input("Select a valid option [1,2,3,4,5]: "))
    return select_option


def create_from_csv(filename):
    try:
        with open(filename, "r") as fPtr:
            reader = csv.reader(fPtr)
            next(reader)  # Skip the header row
            for row in reader:
                create_user_two(row[0], row[1], row[2])
            logging.info(f"Batch user creation from '{filename}' completed successfully.")
    except FileNotFoundError:
        logging.error(f"CSV file '{filename}' not found.")
    except Exception as e:
        logging.error(f"Failed to create users from CSV '{filename}': {e}")


def main():
    option = get_option()
    if option == 5:
        logging.info("Program exited by user.")
        sys.exit()

    uname = input("Enter the username of the user to be processed: ") if option in [1, 2, 4] else None
    if option == 1:
        create_user(uname)
    elif option == 2:
        deletes_user(uname)
    elif option == 3:
        csv_file = input("Enter the path to the CSV file: ")
        create_from_csv(csv_file)
    elif option == 4:
        modify_user(uname)
    else:
        logging.error("Invalid option selected.")


if __name__ == '__main__':
    main()
