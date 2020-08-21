#Import flask
from flask import Flask, jsonify

#Import dependencies for queries to include in endpoints
############################
from matplotlib import style
style.use('seaborn')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import pprint as pp
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
###############################
#Set up connection to sqlite database
## Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
## Declare a base 
Base = automap_base()
## Use base class to reflect Hawaii database tables
Base.prepare(engine, reflect = True)
## Double check connection brought in right tables
Tables = Base.classes.keys()
#print(Tables)
##Save measurement and station table refs to their own variables 
measurement = Base.classes.measurement
station = Base.classes.station
##Create a session to manage transactions to sqlite db
session = Session(engine)
#################################
#Find last 12 months of precipitation data to store on appropriate flask app page
## Start with finding last date in dataset
last = session.query(func.max(measurement.date))
##Initialize list to store last date object when we find it
last_date = []
##Add last date to its list
for l in last:
    last_date.append(l)
##Check work
print(last_date)
##Turn last date into a datetime object
begin = dt.date(2017, 8, 23)
##Find date 12 months before the last date to retrieve last 12 months of precip data & plot results
year_range = begin - dt.timedelta(days = 365)
##Check work
print(year_range)


#Flask setup 
##Initialize Flask app
# app = Flask(__name__)

# @app.route("/")
# def home():
#     print("Server received request for homepage.")
#     return "Available routes:"
#     return "/api/v1.0/precipitation: Returns JSON version of precipitation data."
#     return "/api/v1.0/stations: Returns JSON version of stations in dataset."
#     return "/api/v1.0/tobs: Returns JSON list of temperature observations for the previous year."
#     return "/api/v1.0/<start>` and `/api/v1.0/<start>/<end> Returns JSON list of min, avg, and max temp for a given start or start-end range. If start only, calculates min, avg, and max for all dates greater than and equal to the start date. When given start andn end date, calculates min, avg, and max for dates between the start and end date inclusive."
# @app.route("/api/v1.0/precipitation")
# def precip():
#     print("Server received request for precipitation page.")
#     return jsonify(##Query results as dict##)

# @app.route("/api/v1.0/stations")
# def stations():
#     print("Server received request for stations page.")
#     return jsonify(##Stations dataset##)

# @app.route("/api/v1.0/tobs")
# def temperature():
#     print("Server received request for temperature page.")
#     return jsonify(##json list of temp observations for previous year##)

# @app.route(#"/api/v1.0/<variable for start date>/<variable for end date>")
# def dates():
#     print("Server received request for dates page")
#     return jsonify(##min, avg, max temp of given dates##)

# if __name__ == "__main__":
#     app.run(debug = True)