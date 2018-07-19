import networkx as nx
import bcrypt
import sqlite3
import random
from sys import argv

if __name__ == '__main__':
    
    conn = sqlite3.connect('./' + argv[1], check_same_thread=False)

    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS User (
          id integer primary key autoincrement,
          username text unique,
          password text,
          gender text default null,
          image text default "none",
          age integer default null,
          phone text default null,
          fav_color text default null,
          interests text default null,
          hometown text default null,
          permissions integer default 222222,
          requests text default "[]"
       )""")
    c.execute("""
       CREATE TABLE IF NOT EXISTS Friend (
         id integer primary key autoincrement,
         f1 integer not null,
         f2 integer not null,
         foreign key (f1) references User(id),
         foreign key (f2) references User(id),
         constraint friendship unique (f1, f2)
      )""")
    conn.commit()

    g1 = nx.read_adjlist("g1.txt")
    g2 = nx.read_adjlist("g2.txt")
    g3 = nx.read_adjlist("g3.txt")

    u1 = nx.compose_all([g1,g2,g3])

    print(u1.nodes)
    print(u1.edges)

    """
    for i in range(len(g2.nodes)):
        g2.nodes[i] += len(g1.nodes)-1

    for i in range(len(g2.edges)):
        g2.edges[i][0] += len(g1.nodes)-1
        g2.edges[i][1] += len(g1.nodes)-1

    for i in range(len(g3.nodes)):
        g3.nodes[i] += len(g1.nodes)*2-1

    for i in range(len(g3.edges)):
        g3.edges[i][0] += len(g1.nodes)*2-1
        g3.edges[i][1] += len(g1.nodes)*2-1
        """

    graph = u1

    names = []
    with open("names.txt", "r") as namesFile:
        names = [ n.rstrip("\n") for n in namesFile.readlines()]

    cities = []
    with open("cities.txt", "r") as citiesFile:
        cities = [ c.rstrip("\n") for c in citiesFile.readlines()]

    interests = []
    with open("interests.txt", "r") as interestsFile:
        interests = [ i.rstrip("\n") for i in interestsFile.readlines()]

    colors = ["red", "blue", "yellow", "green", "orange", "purple", "pink"]
    genders = ["male", "female"]
    images = [ str(i) for i in range(28)]

    c = conn.cursor()
    for n in graph.nodes:
        username = names.pop(random.randrange(0, len(names), 1))
        print(username)
        password = username.lower()
        c.execute("""INSERT INTO User(username, password) VALUES (?, ?)""",
                (username, bcrypt.hashpw(password.encode('utf-8'),
                    bcrypt.gensalt())))

        hometown = cities[random.randrange(0, len(cities), 1)]
        fav_color = colors[random.randrange(0, len(colors), 1)]
        gender = genders[random.randrange(0, len(genders), 1)]
        age = random.randrange(15, 95, 1)
        phone = random.randrange(1111111111,9999999999,1)
        interest = ""
        for _ in range(5):
            i = interests[random.randrange(0, len(interests), 1)]
            if i not in interest:
                interest += i + ", "

        image = images.pop(random.randrange(0,len(images),1)) + ".jpg"

        permissions = 0
        for _ in range(6):
            permissions += random.randrange(0,2,1)
            permissions *= 10
        permissions /= 10

        c.execute("""UPDATE User SET age=?,gender=?,phone=?,fav_color=?,
                                     interests=?,hometown=?,image=?,permissions=?
                                     WHERE username=?""",
                                    (age,gender,phone,fav_color,
                                     interest,hometown,image,permissions,username))

    conn.commit()

    c = conn.cursor()
    for e in graph.edges:
        c.execute("""INSERT INTO Friend(f1, f2) VALUES (?, ?)""", (int(e[0])+1, int(e[1])+1))
    conn.commit()

    c = conn.cursor()
    print(argv[2])
    c.execute("""INSERT INTO User(username, password) VALUES (?, ?)""",
            (argv[2].capitalize(), bcrypt.hashpw(argv[2].encode('utf-8'),
                bcrypt.gensalt())))
    conn.commit()
