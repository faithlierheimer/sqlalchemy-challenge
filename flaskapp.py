#Import flask
from flask import Flask, jsonify, request

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
#####print(last_date)
##Turn last date into a datetime object
begin = dt.date(2017, 8, 23)
##Find date 12 months before the last date to retrieve last 12 months of precip data & plot results
year_range = begin - dt.timedelta(days = 365)
##Check work
######print(year_range)
##Query database for last 12 mo of precip data
date = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_range).all()
##Put returned query object into a df, drop any duplicates, check work
precip = pd.DataFrame(date, columns=['date', 'precipitation'])
##print(precip.head())
precip_dict = precip.to_dict('records')
#print(precip_dict)

#################################
#Query database to find active stations & list in descending order of activity
activeStations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).order_by(measurement.station.desc())
activeStations_df = pd.DataFrame(activeStations, columns=['station', 'count'])
activeStations_df = activeStations_df.sort_values(by = ['count'], ascending = False)
##Convert stations df to dictionary
activeStations_dict = activeStations_df.to_dict('records')

###################################
#Query database to find temperature observations for the previous 12 months
temps = session.query(measurement.date, measurement.tobs).filter(measurement.date >= year_range).all()
temps_df = pd.DataFrame(temps, columns = ['date', 'temperature'])
temps_dict = temps_df.to_dict('records')

#Flask setup 
##Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for homepage.")
    return "Available routes:<br/>/api/v1.0/precipitation: Returns JSON version of precipitation data over last 12 months.<br/> /api/v1.0/stations: Returns JSON version of stations in dataset. <br/> /api/v1.0/tobs: Returns JSON list of temperature observations for the previous year. <br/> /api/v1.0/<start>` and `/api/v1.0/<start>/<end> Returns JSON list of min, avg, and max temp for a given start or start-end range. If start only, calculates min, avg, and max for all dates greater than and equal to the start date. When given start and end date, calculates min, avg, and max for dates between the start and end date inclusive. Dates MUST be in following format YYYY-MM-DD."
##This endpoint works as far as I can tell, as of 8/23. 
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for precipitation page.")
    return jsonify(precip_dict)
##This endpoint works! as far as I can tell, as of 8/23.
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for stations page.")
    return jsonify(activeStations_dict)
##This endpoint works! as far as I can tell, as of 8/23
@app.route("/api/v1.0/tobs")
def temperature():
    print("Server received request for temperature page.")
    return jsonify(temps_dict)
#@app.route(#"/api/v1.0/<variable for start date>/<variable for end date>")
#def datesa():
#     print("Server received request for dates page")
#     return jsonify(##min, avg, max temp of given dates##)
#@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/test")
def datesb():
    return """
        <html><body>
            <h2>Thanks for choosing the date request page!</h2>
            <form action="/date">
                What start date do you want to check the temperature for?<br>
                Your answer must be in the YYYY-MM-DD format.<br>
                <input type = 'text' name = 'startdate'><br>
                <input type = 'submit' value = 'Continue'>
            </form>
        </body></html>
        """
@app.route("/date")
def temp_getter():
    startdate = request.args['startdate']
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    Tables = Base.classes.keys()
    measurement = Base.classes.measurement
    station = Base.classes.station
    temps2_list = []
    session = Session(engine)
    ###Somehow this is querying the wrong date and querying the same one no matter what i put in. lol. 
    temps2 = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= str(startdate)).all()
    temps2_df = pd.DataFrame(temps2, columns = ['date', 'min_temp', 'max_temp', 'avg_temp'])
    temps2_dict = temps2_df.to_dict('records')
    return jsonify(temps2_dict)
    # print("Server received request for start date only page.")
    # start = request.args['start date']
    # end = request.args['end date']
    # if (start != None) and (end != None):
    #     temps2 = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    #         filter(measurement.date >= start).filter(measurement.date <= end).all()
    # elif end != None:
    #     temps2 = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    #     filter(measurement.date >= start).all()
    # temps_df2 = pd.DataFrame(temps2, columns = ['date', 'min_temp', 'max_temp', 'avg_temp'])
    # temps_dict2 = temps_df2.to_dict('records')
    # return jsonify(temps_dict2)
if __name__ == "__main__":
    app.run(debug = True)