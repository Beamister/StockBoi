from flask import Flask
from flask import request
from flask import render_template
from scraper import scrape_stock
from analyser import analyse

app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def render_result():
    stock = request.form['stock']
    scraped_data = scrape_stock(stock)
    analysis_result = analyse(scraped_data)
    return render_template('results.html', suggestion=analysis_result)