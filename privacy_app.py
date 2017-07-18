from os import environ, urandom, path, remove as rm_file
from hmac import HMAC as hmac, compare_digest 
import json
import bcrypt
import sqlite3
from hashlib import sha256
from base64 import b64encode, b64decode
from flask import Flask, request, render_template, session, redirect, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = b64decode(environ['SECRET_KEY'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] =  8 * 1024 * 1024 * 1024
app.config['DEBUG'] = False

conn = sqlite3.connect('app.db', check_same_thread=False)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def selectValue(value, user):
    if value not in ["id", "username", "password", "gender", "image", 
                     "age", "phone", "fav_color", "interests", "hometown", 
                     "requests"]:
        return None
    c = conn.cursor()
    return c.execute("""SELECT {v} FROM User WHERE username=? LIMIT 1""".format(v=value),
            (user,)).fetchone()

@app.route('/')
def home():
   return render_template('home.html', authed="username" in session)

@app.route('/d3/')
def graph():
    if "username" not in session:
        return redirect('/')
    c = conn.cursor()
    users = c.execute("""SELECT username,id,gender,image,phone,
                                fav_color,age,permissions,interests,hometown
                                FROM User""").fetchall()
    friends = set(c.execute("""SELECT f1, f2 FROM Friend""").fetchall())
    users.sort(key=lambda u: u[1]) # sort by SQL id
    username = session['username']
    try:
        me = list(filter(lambda u: u[0].capitalize() == username.capitalize(), users))[0]
    except:
        session.pop("username")
        return '', 400
    id = me[1]
    permissions = me[7]
    perms = {
        "image": (permissions//100000),
        "color": (permissions//10000) % 10,
        "age" : (permissions//1000) % 10,
        "gender" : (permissions//100) % 10,
        "interests"   : (permissions// 10) % 10,
        "hometown": permissions % 10
    }
    if "viewing" in session:
        viewing = session["viewing"]
    else:
        viewing = id
    return render_template('graph.html', users=users, friends=list(friends),
                            name=username, id=id, viewing=viewing, perms=perms)

@app.route('/login/', methods=["POST"])
def login():
    if "username" in session:
        session.pop("username")
    username = request.form['name'].capitalize()
    password = request.form['password']
    user_pw = selectValue("password", username)
    if user_pw:
        if bcrypt.checkpw(password.encode('utf-8'), user_pw[0]):
            session['username'] = username
        else:
            flash("Account exists! Incorrect password.")
    else:
        if username == "":
            flash("Can't have an empty username.")
        elif password == "":
            flash("Can't have an empty password.")
        else:
            c.execute("""INSERT INTO User(username, password) VALUES (?, ?)""",
                        (username, bcrypt.hashpw(password.encode('utf-8'),
                          bcrypt.gensalt())))
            conn.commit()
            session['username'] = username
            return redirect("/accountsetup/")
    return redirect('/')

@app.route('/editaccount/', methods=["GET", "POST"])
def editaccount():
    if not "username" in session:
        return redirect('/')
    c = conn.cursor()
    if request.method == "POST":
        gender = request.form['gender']
        fav_color = request.form['color']
        age = request.form['age']
        phone = request.form['phone']
        interests = request.form['interests']
        hometown = request.form['hometown'].capitalize()
        c.execute("""UPDATE User SET age=?,gender=?,phone=?,fav_color=?,
                                     interests=?,hometown=?
                                     WHERE username=?""",
                                    (age,gender,phone,fav_color,
                                     interests,hometown,session['username']))
        conn.commit()
        return redirect("/d3/") 
    user = c.execute("""SELECT fav_color, age, gender, interests, hometown, phone
                        FROM User where username=? LIMIT 1""",
                        (session["username"],)).fetchone()
    userdata = {
            "color":user[0],
            "age":user[1],
            "gender":user[2],
            "interests":user[3],
            "hometown":user[4],
            "phone":user[5]
    }
    return render_template("createaccount.html", target='/editaccount/',**userdata)

@app.route('/accountsetup/', methods=["GET", "POST"])
def accountsetup():
    if not "username" in session:
        return redirect('/')
    if request.method == "POST":
        gender = request.form['gender']
        fav_color = request.form['color']
        age = request.form['age']
        phone = request.form['phone']
        interests = request.form['interests']
        hometown = request.form['hometown'].capitalize()
        c = conn.cursor()
        c.execute("""UPDATE User SET age=?,gender=?,phone=?,
                                     fav_color=?,interests=?,hometown=?
                                     WHERE username=?""",
                                    (age,gender,phone,fav_color,interests,
                                     hometown,session['username']))
        conn.commit()
        return redirect("/")
    return render_template("createaccount.html", target='/accountsetup/',
            gender="", color="", age="", phone="", interests="", hometown="")

@app.route('/addfriend/', methods=["POST"])
def addfriend():
    if not "username" in session:
       return redirect("/")
    id = int(selectValue("id", session['username'])[0])
    targ_id = int(request.values['target'])
    if id == targ_id:
        return "Can't friend yourself", 400
    c = conn.cursor()
    ids = set(c.execute("""SELECT id from User""").fetchall())
    if (targ_id,) not in ids:
        return 'User not found', 400
    friends = set(c.execute("""SELECT f1, f2 from Friend""").fetchall())
    if (id, targ_id) in friends:
        return 'Already friends', 200
    my_requests = set(json.loads(selectValue("requests", session["username"])[0]))
    targ_requests = set(json.loads(c.execute("""SELECT requests
                                                FROM User WHERE id=?""",
                                                (targ_id,)).fetchone()[0]))
    if targ_id in my_requests:
        c.execute("""INSERT INTO Friend(f1, f2) VALUES (?, ?)""", (id, targ_id))
    else:
        targ_requests.add(id)
        c.execute("""UPDATE User set requests=? where id=?""", 
                 (json.dumps(list(targ_requests)), targ_id))
    conn.commit()
    return "Success", 200

@app.route('/logout/')
def logout():
    if "username" in session:
        session.pop("username")
    if "viewing" in session:
        session.pop("viewing")
    return redirect("/")

def ids_are_friends(id1, id2):
    c = conn.cursor()
    is_friend = c.execute("""SELECT count(*) from Friend where (f1=? and f2=?)
                             or (f1=? and f2=?)""", (id1, id2, id2, id1)).fetchone()[0]
    return is_friend > 0

@app.route('/user/<id>/')
def user_info(id):
    if "username" not in session:
        return "Error", 403
    try:
        id = int(id)
    except:
        return json.dumps({}), 200
    c = conn.cursor()
    user = c.execute("""SELECT username, fav_color, age, gender,image, interests, hometown,
                        permissions,requests FROM User where id=? LIMIT 1""",
                        (int(id),)).fetchone()
    if user is None:
        return json.dumps({}), 200
    usermap = {"name":user[0], "color":user[1], "age":user[2], "gender":user[3],
                "image":user[4], "interests":user[5], "hometown":user[6]}
    session["viewing"] = id
    my_id = selectValue("id", session["username"])[0]
    is_me = my_id == id
    is_friend = is_me or ids_are_friends(my_id, id)
    is_fof = is_friend or bool(c.execute("""SELECT l.f1, l.f2, r.f1, r.f2 from
                                Friend as l, Friend as r where
                                (l.f1=? and l.f2=r.f1 and r.f2=?) or
                                (l.f2=? and l.f1=r.f1 and r.f2=?) or
                                (l.f1=? and l.f2=r.f2 and r.f1=?) or
                                (l.f2=? and l.f1=r.f2 and r.f1=?)""",
                                (my_id, id, my_id, id, my_id, id, my_id,id)).fetchall())
    permissions = user[7]
    show = {}
    # ZNJP PERMISSION STUFF IS HERE
    perms = {
        "image": (permissions//100000),
        "color": (permissions//10000) %10,
        "age" : (permissions//1000) % 10,
        "gender" : (permissions//100) % 10,
        "interests"   : (permissions// 10) % 10,
        "hometown": permissions % 10
    }
    if is_me:
        show = usermap
    else:
        for k in perms:
            if perms[k] == 0:
                if is_friend:
                    show[k] = usermap[k]
                else:
                    show[k] = "hidden"
            elif perms[k] == 1:
                if is_friend or is_fof:
                    show[k] = usermap[k]
                else:
                    show[k] = "hidden"
            elif perms[k] == 2:
                show[k] = usermap[k]
        show["name"] = usermap["name"]
    requested = set(json.loads(user[8]))
    my_requested = set(json.loads(c.execute("""SELECT requests FROM User
                                               WHERE id=?""",
                                               (my_id,)).fetchone()[0]))
    if my_id in requested:
        show["requested"] = 2 # I requested targ
    elif id in my_requested:
        show["requested"] = 1 # targ requested me
    else:
        show["requested"] = 0 # neither or both
    return json.dumps(show), 200

@app.route('/pic/<filename>')
def profile_image(filename):
    # ZNJP
    # fun thing to do: when image settings dictate, users see
    # hidden.jpg instead of the profile image, but using 
    # direct object references at /pic/<filename> they could
    # bypass privacy settings to view people's profile images
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/profile_upload/', methods=['POST'])
def profile_pic_upload():
    if 'username' not in session or 'profile_image' not in request.files:
        return redirect('/d3/')
    user = session['username']
    file = request.files['profile_image']
    if file.filename == '':
        return redirect('/d3/')
    if file and allowed_file(file.filename):
        fname = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], fname))
        c = conn.cursor()
        c.execute("""UPDATE User SET image=? WHERE username=?""",
                        (fname,user))
        conn.commit() 
    return redirect("/d3/")

@app.route('/profile_pic_teardown/', methods=['POST'])
def profile_pic_teardown():
    if 'username' not in session:
        return redirect('/d3/')
    user = session['username']
    c = conn.cursor()
    try:
        old_img = selectValue("image", user)[0]
    except IndexError:
        old_img = None
    c.execute("""UPDATE User SET image=? WHERE username=? LIMIT 1""",
                        ("none",user))
    conn.commit()
    if old_img:
        rm_file(path.join(app.config["UPLOAD_FOLDER"], old_img))
    return redirect('/d3/')

def controlStringToInt(string):
    if string == "friends":
        return 0
    elif string == "fof":
        return 1
    else:
        return 2

@app.route("/control_change/", methods=["POST"])
def control_change():
    if "username" not in session:
        return "", 400
    #values as color;age;gender
    values = request.form.getlist("control")

    value_list = values[0].split(';')
    permissions = 0
    for v in value_list:
        permissions = permissions + controlStringToInt(v)
        permissions = permissions * 10
    permissions = permissions/10

    user = session['username']

    c = conn.cursor()
    c.execute("""UPDATE User SET permissions=? WHERE username=?""", (permissions,user))
    conn.commit()

    return "", 200

if __name__ == '__main__':
    app.run(debug=True, port=8081)
