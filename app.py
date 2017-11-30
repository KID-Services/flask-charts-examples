import json
import datetime, calendar
from io import BytesIO
from flask import Flask, g, make_response, render_template
    
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import numpy as np

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

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

def get_x_y_coords():
    data = models.PeopleServed.select().order_by(models.PeopleServed.date.desc()).limit(15).dicts()
    x=[]
    y=[]
    for item in data:
        x.append(item['date'])
        y.append(item['people'])
    return x, y
    

@app.route('/d3js')
def d3js():
    data = get_data()
    return render_template('d3js.html', data=data)


@app.route('/bokeh')
def bokeh():
    # prepare some data
    x, y = get_x_y_coords()

    # create a new plot with a title and axis labels
    p_fig = figure(
        title="people per day",
        x_axis_label='date',
        y_axis_label='people',
        plot_width=600,
        plot_height=600,
        x_axis_type="datetime"
    )

    # add a line renderer with legend and line thickness
    p_fig.line(
        x,
        y,
        legend="People per Day",
        line_width=2,
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p_fig)
    return render_template(
        'bokeh.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

@app.route('/maplotlib')
def matplotlib():
    return render_template('matplotlib.html')

@app.route('/images/maplotlib.png')
def matplotlib_image():
    fig=Figure()
    ax=fig.add_subplot(111)
    x, y = get_x_y_coords()
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
