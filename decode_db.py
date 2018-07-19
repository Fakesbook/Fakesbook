from sys import argv
import ceasar
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('./' + argv[1], check_same_thread=False)
    c = conn.cursor()
    users = c.execute("""SELECT username,gender,image,
                                fav_color,interests,hometown
                                FROM User""").fetchall()
    for u in users:
        original_user = u[0]
        new_u = []
        for i in range(len(u)):
            new_u.append(ceasar.decode(u[i], int(argv[2])))

        c.execute("""UPDATE User SET username=?,gender=?,image=?,fav_color=?,
                                     interests=?,hometown=?
                                     WHERE username=?""",
                                    (new_u[0],new_u[1],new_u[2],new_u[3],
                                     new_u[4],new_u[5],original_user))
    conn.commit()
