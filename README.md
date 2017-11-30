# flask-charts-examples

Examples of different chart libraries with flask

The libraries used in these examples are:

* [d3js](https://d3js.org/)
* [matplotlib (generates png)](https://matplotlib.org/)
* [bokeh](https://bokeh.pydata.org/en/latest/)
* [flot](http://www.flotcharts.org/)

More options for future:

* [Chart js](http://www.chartjs.org/)

Nice dashboards:

* [Responsive dashboard templates](http://keen.github.io/dashboards/)

## Getting Started

1. Create a virtual environment

        mkvirtualenv --python=python3.6 flask-charts

2. Install requirements

        pip install -r requirements.txt

4. Create a postgres database

        psql
        CREATE DATABASE flask_chart_examples;

5. Create the data

        python setup_data.py

## Run the simple app

        python simple_app.py

### Sources

* [d3js simpleline chart](https://gist.github.com/d3noob/402dd382a51a4f6eea487f9a35566de0)