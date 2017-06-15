from sys import argv
import bcrypt
import pathlib
import sqlite3

def reset_pw(filename):
    user = input("Input username: ").capitalize()
    pw = input("Input new password: ").encode('utf-8')
    hsh = bcrypt.hashpw(pw, bcrypt.gensalt())
    conn = sqlite3.connect(filename, check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE User SET password=? where username=?", (hsh, user))
    conn.commit()

if __name__ == '__main__':
    if len(argv) == 2:
        if pathlib.Path(argv[1]).is_file():
            reset_pw(argv[1])
            print("Done.")
        else:
            print("No database file at %s" % argv[1])
    else:
        print("Usage: python3 reset_password.py <app.db>")
