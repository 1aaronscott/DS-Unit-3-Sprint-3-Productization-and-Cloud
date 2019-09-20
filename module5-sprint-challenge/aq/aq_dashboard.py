"""Basic Flask app showing air quality reading from Los Angeles, Chile.
"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import openaq

APP = Flask(__name__)  # upfront since no longer using models.py
DB = SQLAlchemy(APP)  # was in models.py for twitoff


class Record(DB.Model):
    """Create and config database."""
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    city = DB.Column(DB.String(60))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DATE: {}, VALUE: {}>'.format(self.datetime, self.value)


def create_app():
    """Create and config routes for the air quality flask app."""
    APP.config['ENV'] = config('ENV')
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    api = openaq.OpenAQ()

    @APP.route('/')
    def root():
        """Main page showing database records."""
        records = Record.query.filter(Record.value >= 10).all()
        return render_template('base.html', records=records)

    @APP.route('/refresh')
    def refresh():
        """Clear out the database and populate with current data."""
        DB.drop_all()
        DB.create_all()
        city = 'Los Angeles'
        #city = 'Pittsburgh'
        #city = 'St. Louis'
        get_city_data(city, api)
        DB.session.commit()
        return render_template('refresh.html')

    def get_city_data(city, api):
        """Use the api to get a city's data and write to the database.
        could use the status code for error checking instead of tossing it."""
        _, body = api.measurements(city=city, parameter='pm25')
        city_data = api_json_to_tuples(body)
        for cur_line in city_data:
            db_record = Record(
                city=city, datetime=cur_line[0], value=cur_line[1])
            DB.session.add(db_record)

    def api_json_to_tuples(body):
        """Converts the json in the api to a list of tuples."""
        results = body['results']
        date_values = []
        for result in results:
            cur_date_value = (str(result['date']['utc']), result['value'])
            date_values.append(cur_date_value)
        return date_values

    return APP

# plan to add US cities (api only returns 100)
# 1. add city column in database
# 2. get list of available US cities in refresh route:
#    resu = body['results']
#    for line in range(0, len(resu)):
#        current_city = resu[line]['city']
# 3. call get_city_data with current_city etc
# 4. on main page show a dropdown with list of possible cities
# 5. pass city name to base.html
