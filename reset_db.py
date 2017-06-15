from sys import argv
import pathlib
import sqlite3

def reset_db(filename):
    """ DROP TABLES """
    conn = sqlite3.connect(filename, check_same_thread=True)
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS User""")
    c.execute("""DROP TABLE IF EXISTS Friend""")
    conn.commit()

if __name__ == '__main__':
    if len(argv) == 2:
        if pathlib.Path(argv[1]).is_file():
            if ('y' in input("This will drop the database in %s. Continue? [y/N] " % argv[1])):
                reset_db(argv[1])
                print("Dropped.")
            else:
                print("Cancelled.")
        else:
            print("No database file at %s" % argv[1])
    else:
        print("Usage: python3 reset_db.py <app.db>")
