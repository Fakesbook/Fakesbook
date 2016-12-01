
from flask import Flask, request, render_template, session, redirect

import sqlite3
conn = sqlite3.connect('app.db')

app = Flask(__name__)
debug = True

@app.route('/')
def home():
   return render_template('index.html')
   #return render_template('home.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
   username = request.form['name']
   password = request.form['password']
   return render_template("login.html", u=username, p=password)

if __name__ == '__main__':
    app.run(debug=debug, port=8080)    
