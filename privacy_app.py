from os import environ
from flask import Flask, request, render_template, session, redirect

import sqlite3
conn = sqlite3.connect('app.db')

app = Flask(__name__)
app.secret_key = environ['SECRET_KEY']
debug = True

@app.route('/')
def home():
   return render_template('index.html', authed="username" in session)
   #return render_template('home.html')

@app.route('/d3/')
def demo():
   return render_template('demo.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
   username = request.form['name']
   password = request.form['password']
   session['username'] = username
   return render_template("login.html", u=username, p=password)

if __name__ == '__main__':
    app.run(debug=debug, port=8080)    
