from os import environ, urandom
from hmac import HMAC as hmac, compare_digest 
from hashlib import sha256
from base64 import b64encode, b64decode
from flask import Flask, request, render_template, session, redirect

import sqlite3
conn = sqlite3.connect('app.db', check_same_thread=False)

def compare_passwords(a, b):
   """ VERY safely compare passwords """
   try:
      pw = b64encode(urandom(32))
      return compare_digest(hmac(pw, a.encode(), sha256).hexdigest(),
            hmac(pw, b.encode(), sha256).hexdigest())
   except UnicodeEncodeError:
      return False

c = conn.cursor()
c.execute("""DROP TABLE IF EXISTS User""")
c.execute("""
   CREATE TABLE User (
      id integer primary key autoincrement,
      username text unique,
      password text,
      gender text defaul null,
      image blob default null,
      birthdate text default null,
      phone text defaul null,
      fav_color text default null
   )""")

c.execute("""insert into User(username, password) values ('max', 'foo')""")
conn.commit()

app = Flask(__name__)
app.secret_key = b64decode(environ['SECRET_KEY'])
debug = True

@app.route('/')
def home():
   return render_template('index.html', authed="username" in session)

@app.route('/d3/')
def demo():
   return render_template('demo.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
   if request.method == 'POST':
      username = request.form['name']
      password = request.form['password']
      user_pw = c.execute("""
         SELECT password FROM User
         WHERE username=? LIMIT 1""", (username,)).fetchone()
      if user_pw and compare_passwords(password, user_pw[0]):
         session['username'] = username
         return render_template("login.html", u=username, p=password)
   return redirect('/')

@app.route('/register/', methods=["POST"])
def register():
   username = request.form['name']
   password = request.form['password']
   c = conn.cursor()
   c.execute("""INSERT INTO User(username, password) VALUES (?, ?)""", (username, password))
   conn.commit()
   return redirect("/login/")

@app.route('/logout/')
def logout():
   session.pop("username")
   return redirect("/")

@app.route('/users/<name>/')
def user_info(name):
    user = c.execute("""SELECT * from User where username=? LIMIT 1""",
                        (name,)).fetchone()
    print(user) # TODO remove
    return render_template("user.html", user=user)

if __name__ == '__main__':
    app.run(debug=debug, port=8080)    
