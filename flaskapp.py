#Import flask
from flask import Flask, jsonify

#Flask setup 
##Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for homepage.")
    return "Available routes:"
    return "/api/v1.0/precipitation: Returns JSON version of precipitation data."
    return "/api/v1.0/stations: Returns JSON version of stations in dataset."
    return "/api/v1.0/tobs: Returns JSON list of temperature observations for the previous year."
    return "/api/v1.0/<start>` and `/api/v1.0/<start>/<end> Returns JSON list of min, avg, and max temp for a given start or start-end range. If start only, calculates min, avg, and max for all dates greater than and equal to the start date. When given start andn end date, calculates min, avg, and max for dates between the start and end date inclusive."
@app.route("/api/v1.0/precipitation")
def precip():
    print("Server received request for precipitation page.")
    return jsonify(##Query results as dict##)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for stations page.")
    return jsonify(##Stations dataset##)

@app.route("/api/v1.0/tobs")
def temperature():
    print("Server received request for temperature page.")
    return jsonify(##json list of temp observations for previous year##)

@app.route(#"/api/v1.0/<variable for start date>/<variable for end date>")
def dates():
    print("Server received request for dates page")
    return jsonify(##min, avg, max temp of given dates##)
