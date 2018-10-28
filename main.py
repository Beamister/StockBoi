from flask import Flask
from flask import request
from flask import render_template
from scraper import scrape
from analyser import analyse

app = Flask(__name__)


# set up symbols as a dictionary
symbols_dict = {}
with open('static/NASDAQ.txt', mode='r') as infile:
    for line in infile:
        (key, val) = line.strip().split('	', 1)
        symbols_dict[key] = val.upper()

@app.route('/')
def render_home():
    return render_template('index.html')


@app.route('/result')
def render_result():
    if request.method=='GET':
        # this gets stock_dict_unset as key value pair ('stock_name', value)
        stock_dict_unset = request.args
        stock_dict = {}

        if (stock_dict_unset['stock_name'].upper() in symbols_dict):
            print(stock_dict_unset['stock_name'].upper() + " is a key")
            stock_dict['stock_name'] = stock_dict_unset['stock_name'].upper()
            print(stock_dict)
        else:
            for key, value in symbols_dict.iteritems():
                if stock_dict_unset['stock_name'].upper() in value:
                    stock_dict['stock_name'] = key
                    print("stock name changed from " + stock_dict_unset['stock_name'].upper() + " to " + key)
                    print (stock_dict['stock_name'])
                    break

        scraped_data = scrape(stock_dict['stock_name'])
        analysis_result = analyse(scraped_data)
        return render_template('results.html',stock_dict=stock_dict,analysis_result=analysis_result)
    else:
        render_template('error.html')
