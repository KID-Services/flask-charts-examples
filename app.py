import json
from flask import Flask, g, render_template

import models

app = Flask(__name__)


def before_request():
    '''Connect to the database before each request'''
    g.db = models.DATABASE
    g.db.get_conn()


def after_request(response):
    '''Close the connection to the db'''
    g.db.close
    return response


def get_data():
    data = models.PeopleServed.select().dicts()
    people_list = []
    for item in data:
        people_list.append({'data': str(item['date']), 'people': item['people']})
    return people_list


@app.route('/d3js')
def d3js():
    data = get_data()
    return render_template('d3js.html', data=data)


@app.route('/bokeh')
def bokeh():
    data = get_data()
    return render_template('bokeh.html', data=data)


@app.route('/maplotlib')
def matplotlib():
    data = get_data()
    return render_template('matplotlib.html', data=data)


@app.route('/flot')
def flot():
    data = get_data()
    return render_template('flot.html', data=data)


@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    models.initialise()
    app.run(debug=True)
