from sys import argv
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('./' + argv[1], check_same_thread=False)
    c = conn.cursor()
    users = c.execute("""SELECT username,gender,image,
                                fav_color,interests,hometown
                                FROM User""").fetchall()
    for u in users:
        print(u)
