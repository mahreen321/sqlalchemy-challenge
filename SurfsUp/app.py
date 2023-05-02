# Import the dependencies.
import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists

from flask import Flask, jsonify


# Set up database engine for Flask app
engine = create_engine("sqlite:////Users/mahreenayaz/Documents/hawaii.sqlite")
Base = automap_base()

# Reflect database into classes
Base.prepare(engine, reflect=True)

# Set class variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Flask app, all routes go after this code
app = Flask(__name__)

# Define welcome route
@app.route("/")

def welcome():
    return(
    '''
   Hi, Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Precipitation Route
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# check website changes, (http://127.0.0.1:5000/)

#Stations Route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# Monthly Temperature Route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Stations Route
@app.route("/api/v1.0/<start>")
def start_stats(start):
    """Return the minimum, average, and maximum temperatures for all dates greater than or equal to the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    stats_list = [{"start_date": start, "end_date": "latest", "TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}]
    return jsonify(stats_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_stats(start, end):
    """Return the minimum, average, and maximum temperatures for dates between the start and end date (inclusive)."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    stats_list = [{"start_date": start, "end_date": end, "TMIN": results[0][0], "TAVG": results[0][1], "TMAX": results[0][2]}]
    return jsonify(stats_list)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
