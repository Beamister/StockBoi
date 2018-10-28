from flask import Flask
from flask import request
from flask import render_template
from scraper import scrape_stock
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
            print(stock_dict_unset['stock_name'] + " is a key")
            stock_dict['stock_name'] = stock_dict_unset['stock_name'].upper()
            print(stock_dict)
        else:
            for key, value in symbols_dict.iteritems():
                if stock_dict_unset['stock_name'].upper() in value:
                    stock_dict['stock_name'] = key
                    print("stock name changed from " + stock_dict_unset['stock_name'] + " to " + key)
                    print (stock_dict['stock_name'])
                    break

        # waiting for bois to finish
        # scraped_data = scrape_stock(stock_dict['stock_name'])

        # temp input to test and submit with
        scraped_data={'metadata':{'name':'nameplaceholder',
                                  'article_count':3},
                      'articles':{0:{'headline':'headline0placeholed',
                                     'text': 'text0placeholed',
                                     'datetime':'datetime0placeholder'
                                    },
                                  1:{'headline':'headline1placeholed',
                                     'text': 'text1placeholed',
                                     'datetime':'datetime1placeholder'
                                    },
                                  2:{'headline':'headline2placeholed',
                                     'text': 'text2placeholed',
                                     'datetime':'datetime2placeholder'
                                    },
                                  3:{'headline':'headline3placeholed',
                                     'text': 'text3placeholed',
                                     'datetime':'datetime3placeholder'
                                    },
                                  4:{'headline':'headline4placeholed',
                                     'text': 'text4placeholed',
                                     'datetime':'datetime4placeholder'
                                    },
                                  5:{'headline':'headline5placeholed',
                                     'text': 'text5placeholed',
                                     'datetime':'datetime5placeholder'
                                    },
                                  6:{'headline':'headline6placeholed',
                                     'text': 'text6placeholed',
                                     'datetime':'datetime6placeholder'
                                    }
                                 }
                     }
        analysis_result = analyse(scraped_data)
        print(analysis_result)
        return render_template('results.html',stock_dict=stock_dict,analysis_result=analysis_result)
    else:
        render_template('error.html')
