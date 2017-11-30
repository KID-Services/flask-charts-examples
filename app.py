import json
import datetime, calendar
from io import BytesIO
from flask import Flask, g, make_response, render_template
    
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

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
    data = models.PeopleServed.select().order_by(models.PeopleServed.date.desc()).limit(5).dicts()
    people_list = []
    for item in data:
        people_list.append({'date': str(item['date']), 'people': item['people']})
    return people_list

def get_list_data():
    data = models.PeopleServed.select().order_by(models.PeopleServed.date.desc()).limit(5).dicts()
    people_list = []
    for item in data:
        people_list.append([str(item['date']), item['people']])
    return people_list


def get_flot_data():
    '''Flot requires unix timestamps'''
    data = models.PeopleServed.select().order_by(models.PeopleServed.date.desc()).limit(15).dicts()
    people_list = []
    for item in data:
        time = calendar.timegm(item['date'].timetuple()) * 1000
        people_list.append([time, item['people']])
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
    return render_template('matplotlib.html')

@app.route('/images/maplotlib.png')
def matplotlib_image():
    fig=Figure()
    ax=fig.add_subplot(111)
    data = models.PeopleServed.select().order_by(models.PeopleServed.date.desc()).limit(15).dicts()
    x=[]
    y=[]
    for item in data:
        x.append(item['date'])
        y.append(item['people'])
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route('/flot')
def flot():
    data = get_flot_data()
    return render_template('flot.html', data=data)


@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    models.initialise()
    app.run(debug=True)
