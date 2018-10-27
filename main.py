from flask import Flask
from flask import render_template
from scraper import scrape
from analyser import analyse

app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/result/<stock')
def render_result(stock=""):
    scraped_data = scrape(stock)
    analysis_result = analyse(scraped_data)
    return render_template('results.html', suggestion=analysis_result)