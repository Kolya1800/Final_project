#!/usr/bin/python
import crypt
import csv
import getpass
import pwd
import subprocess
import sys
import logging

# Set up logging
logging.basicConfig(
    filename="sys_admin.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def user_exists(username) -> bool:
    """Check if a user exists in the system."""
    try:
        pwd.getpwnam(username)
        logging.info(f"Checked existence of user '{username}': EXISTS.")
        return True
    except KeyError:
        logging.info(f"Checked existence of user '{username}': DOES NOT EXIST.")
        return False


def create_user(username: str):
    """Create a single user with optional root access."""
    password = getpass.getpass(f"Enter the password for this user '{username}': ")
    role = input(f"Give user '{username}' root access (y/n)? ")
    en_pwd = crypt.crypt(password)

    if user_exists(username):
        logging.warning(f"Cannot create user '{username}': Already exists.")
    else:
        try:
            subprocess.call(["useradd", "-p", en_pwd, username])
            logging.info(f"User '{username}' created successfully.")
            if role.lower() == "y":
                subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Granted root access to user '{username}'.")
        except Exception as e:
            logging.error(f"Error creating user '{username}': {e}")


def modify_user(username):
    """Modify user details: password, role, or both."""
    if not user_exists(username):
        logging.warning(f"Cannot modify user '{username}': User does not exist.")
        return

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
                logging.info(f"Granted root access to user '{username}'.")
            except Exception as e:
                logging.error(f"Failed to assign root access to user '{username}': {e}")

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
                logging.info(f"Granted root access to user '{username}'.")
            except Exception as e:
                logging.error(f"Failed to assign root access to user '{username}': {e}")


def create_user_two(username, role, password):
    """Create a single user from CSV with a role."""
    if user_exists(username):
        logging.warning(f"User '{username}' exists. Skipping creation.")
    else:
        en_pwd = crypt.crypt(password)
        try:
            subprocess.call(["useradd", "-p", en_pwd, username])
            logging.info(f"User '{username}' created successfully.")
            if role.lower() == "admin":
                subprocess.call(["usermod", "-aG", "root", username])
                logging.info(f"Granted admin privileges to user '{username}'.")
        except Exception as e:
            logging.error(f"Error creating user '{username}': {e}")


def deletes_user(username):
    """Delete a user from the system."""
    if user_exists(username):
        try:
            subprocess.call(["userdel", "-r", username])
            logging.info(f"User '{username}' deleted successfully.")
        except Exception as e:
            logging.error(f"Failed to delete user '{username}': {e}")
    else:
        logging.warning(f"Cannot delete user '{username}': Does not exist.")


def get_option():
    """Display menu options and get user input."""
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


def main():
    """Main function to run the script."""
    option = get_option()
    if option == 1:
        uname = input("Enter the username to create: ")
        create_user(uname)
    elif option == 2:
        uname = input("Enter the username to delete: ")
        deletes_user(uname)
    elif option == 3:
        csv_file = input("Enter the path to the CSV file: ")
        create_from_csv(csv_file)
    elif option == 4:
        uname = input("Enter the username to modify: ")
        modify_user(uname)
    elif option == 5:
        logging.info("Program exited by user.")
        sys.exit()


if __name__ == "__main__":
    main()
