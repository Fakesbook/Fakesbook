from os import environ, urandom
from hmac import HMAC as hmac, compare_digest 
import bcrypt
from hashlib import sha256
from base64 import b64encode, b64decode
from flask import Flask, request, render_template, session, redirect, flash

import sqlite3
conn = sqlite3.connect('app.db', check_same_thread=False)

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
conn.commit()

app = Flask(__name__)
app.secret_key = b64decode(environ['SECRET_KEY'])
debug = True

@app.route('/')
def home():
   return render_template('home.html', authed="username" in session)

@app.route('/d3/')
def graph():
   c = conn.cursor()
   users = c.execute("""SELECT username,gender,image,birthdate,phone,fav_color FROM User""").fetchall()
   users.sort(key=lambda u: u[0]) # sort by SQL id
   friends = {0:1} # TODO create demo friend connections, then real ones
   return render_template('demo.html', users=users, len=len(users), friends=friends)

@app.route('/login/', methods=["GET", "POST"])
def login():
   if request.method == 'POST' and "username" not in session:
      username = request.form['name'].capitalize()
      password = request.form['password']
      user_pw = c.execute("""
         SELECT password FROM User
         WHERE username=? LIMIT 1""", (username,)).fetchone()
      if user_pw and bcrypt.checkpw(password.encode('utf-8'), user_pw[0]):
         session['username'] = username
      else:
         flash("Incorrect username/password")
   return redirect('/')

@app.route('/accountsetup/', methods=["GET", "POST"])
def accountsetup():
    if not "username" in session:
        return redirect('/')
    if request.method == "POST":
        gender = request.form['gender']
        favcolor = request.form['color']
        birthday = request.form['birthday']
        age = request.form['age']
        phone = request.form['phone']
        c = conn.cursor()
        c.execute("""UPDATE User SET gender=?,birthdate=?,phone=?,fav_color=? WHERE username=?""", (gender,birthday,phone,favcolor,session['username']))
        conn.commit()
        return redirect("/")
    return render_template("createaccount.html")

@app.route('/addfriend/', methods=["POST"])
def addfriend():
    if not "username" in session:
       return redirect("/")
    # TODO

@app.route('/register/', methods=["POST"])
def register():
   if "username" in session:
      return redirect('/')
   username = request.form['name'].capitalize()
   password = request.form['password']
   c = conn.cursor()
   user = c.execute("""
         SELECT username FROM User
         WHERE username=? LIMIT 1""", (username,)).fetchone()
   if user:
      flash("That username is already taken.")
      return redirect("/")
   c.execute("""INSERT INTO User(username, password) VALUES (?, ?)""", (username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())))
   conn.commit()
   session['username'] = username
   return redirect("/accountsetup/")

@app.route('/logout/')
def logout():
   session.pop("username")
   return redirect("/")

@app.route('/user/<name>/')
def user_info(name):
    c = conn.cursor()
    user = c.execute("""SELECT * from User where username=? LIMIT 1""",
                        (name.capitalize(),)).fetchone()
    return render_template("user.html", user=user)

if __name__ == '__main__':
    app.run(debug=debug, port=8080)    
