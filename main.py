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
        analysis_result = {'metadata':{'overall_score':0.0},
                           'articles':{ 0:{ 'headline':'Article headline 1',
                                            'text1':'this is the first text',
                                            'text2':'the second one',
                                            'text3':'and the third text',
                                            'date_time':'02_01_2018 17:50',
                                            'certainty':0.46},
                                        1:{'headline':'Article headline 2',
                                            'text1':'text uno',
                                            'text2':'dos',
                                            'text3':'tres',
                                            'date_time':'02_01_2019 16:45',
                                            'certainty':0.63},
                                        2:{'headline':'Article headline 3',
                                            'text1':'one',
                                            'text2':'two',
                                            'text3':'three',
                                            'date_time':'02_01_2019 16:45',
                                            'certainty':0.88},
                                        3:{'headline':'Article headline 1',
                                            'text1':'this is the first text',
                                            'text2':'the second one',
                                            'text3':'and the third text',
                                            'date_time':'02_01_2018 17:50',
                                            'certainty':0.46},
                                        4:{'headline':'Article headline 2',
                                            'text1':'text uno',
                                            'text2':'dos',
                                            'text3':'tres',
                                            'date_time':'02_01_2019 16:45',
                                            'certainty':0.63}
                                      }
                          }
        return render_template('results.html',stock_dict=stock_dict,analysis_result=analysis_result)
    else:
        render_template('error.html')
