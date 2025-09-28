#!/usr/bin/python3
import argparse
import sys
import crypt
import pwd
import subprocess


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
    parser.add_argument("-u", "--username", type=str, action="store", help="Assign username")
    parser.add_argument("-p", "--password", type=str, action="store", help="Assign password")
    parser.add_argument("-r", "--role", type=str, action="store", help="Assign role: [guest, admin]")

    args = parser.parse_args()

    if args.option == "user":
        if not args.username or not args.password or not args.role:
            print("You must include the username, password, and role.")
            sys.exit(1)
        else:
            create_user(args.username, args.password, args.role)
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


if __name__ == '__main__':
    main()
