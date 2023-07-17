# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()


# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return 12 months of precipitation and date data"""
    year_date_prec = session.query(measurement.date, measurement.prcp).filter(measurement.date.between('2016-08-23', '2017-08-23'))

    session.close()

    # Create a dictionary with date as key and prcp as value
    precipitations = []
    for date, prcp in year_date_prec:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitations.append(precipitation_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session = Session(engine)

    # Return list of stations
    stations = session.query(station.station).all()

    session.close()

    #convert to normal list
    all_names = list(np.ravel(stations))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    temp = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').all()

    session.close()

    #convert to dictionary
    tobs_list = []
    for date, tobs in temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        tobs_list.append(temp_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def route(start_date, end_date):
   
    temperature = (session.query(measurement.tobs).filter(measurement.date.between(start_date, end_date)).all())
    #minimum = session.query(measurement.tobs, func.min(measurement.tobs)).filter(measurement.date.between(start_date, end_date))
    session.close()

    #temp_min = func.min(temp)
    #temp_max = func.max(temp)
    #temp_avg = func.avg(temp)

    all_temp = list(np.ravel(temperature))
    return all_temp
    #average = min(list(np.ravel(temperature)))
    #return average
    #return jsonify(minimum)
    
    #minimumtemp = list(np.ravel(minimum))
    #return minimumtemp
if __name__ == '__main__':
    app.run(debug=True)



