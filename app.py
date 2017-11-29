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
    return render_template('index.html')

if __name__ == '__main__':
    models.initialise()
    app.run(debug=True)
