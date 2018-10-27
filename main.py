from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/result/<stock_name>')
def render_result():
    return render_template('results.html')