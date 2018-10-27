from flask import Flask
from flask import request
from flask import render_template
from scraper import scrape
from analyser import analyse
import ast

app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('index.html')

#@app.route('/result')
#def render_result():
#    if request.method=='GET':
#        stock_dict = request.args
#        scraped_data = scrape(stock_dict['stock_name'])
#        analysis_result = analyse(scraped_data)
#        return render_template('results.html',stock_dict=stock_dict,analysis_result=analysis_result)
#    else:
#        render_template('error.html')

@app.route('/result')
def render_result():
    if request.method=='GET':
        stock_dict = request.args
        scraped_data = scrape(stock_dict['stock_name'])
        analysis_result = {'metadata':{'overall_score':0.8},
                           '0':{'headline':'article headline 1',
                                'text1':'this is the first text',
                                'text2':'the second one',
                                'text3':'and the third text',
                                'date_time':'02_01_2018 17:50',
                                'certainty':0.76},
                           '1':{'headline':'article headline 2',
                                'text1':'text uno',
                                'text2':'dos',
                                'text3':'tres',
                                'date_time':'02_01_2019 16:45',
                                'certainty':0.43},
                           '2':{'headline':'article headline 3',
                                'text1':'one',
                                'text2':'two',
                                'text3':'three',
                                'date_time':'02_01_2019 16:45',
                                'certainty':0.88}
                          }
        return render_template('results.html',stock_dict=stock_dict,analysis_result=analysis_result)
    else:
        render_template('error.html')