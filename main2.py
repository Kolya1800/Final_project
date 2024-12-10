#!/usr/bin/python3
import argparse
import sys
import crypt
import pwd
import subprocess
import csv


def user_exists(username) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except:
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

        if args.create:
            if not args.username or not args.password or not args.role:
                print("You must include the username, password, and role.")
                sys.exit(1)
            else:
                create_user(args.username, args.password, args.role)

        if args.create_batch:
            if not args.filename:
                print("You must include the filename.")
            else:
                create_from_csv(args.filename)

        if args.delete:
            if not args.username:
                print("You must include the username.")
                sys.exit(1)
            else:
                deletes_user(args.username)

        if args.update:
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
        print(f"The user with name '{username}' already exists. Please try again.")
    else:
        subprocess.call(["useradd", "-p", en_pwd, username])
    if role == "admin":
        subprocess.call(["usermod", "-g", "root", username])


def create_user_two(username: str, role: str, password: str):
    if user_exists(username):
        print(f"This user {username} exists. It was not created.")
    else:
        en_pwd = crypt.crypt(password)
        subprocess.call(["useradd", "-p", en_pwd, username])
        if role == "admin":
            subprocess.call(["usermod", "-g", "root", username])


def create_from_csv(filename: str):
    with open(filename, "r") as fPtr:
        reader = csv.reader(fPtr)
        next(reader)
        for row in reader:
            create_user_two(row[0], row[1], row[2])
        fPtr.close()


def deletes_user(username: str):
    if user_exists(username):
        subprocess.call(["deluser", "--remove-all-files", username])
    else:
        print(f"The user '{username}' does not exist and cannot be deleted.")


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
