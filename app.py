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


@app.route('/')
def index():
    data = models.PeopleServed.select().dicts()
    people_list = []
    for item in data:
        people_list.append([str(item['date']), item['people']])
    return render_template('index.html', data=json.dumps(people_list))

if __name__ == '__main__':
    models.initialise()
    app.run(debug=True)
