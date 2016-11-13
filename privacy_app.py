
from flask import Flask, request, render_template

app = Flask(__name__)
debug = True

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=debug, port=8080)    
