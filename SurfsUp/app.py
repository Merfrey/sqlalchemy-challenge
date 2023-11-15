# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################


# create engine to SQLalchemy file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with = engine)
Base.classes.keys()

# Save references to each table
MeasureReference = Base.classes.measurement
StationReference = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
#inspector = inspect(engine)
#inspector.get_table_names()

#################################################
# Flask Setup
app = Flask(__name__)

#################################################



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    # there is some code here

    return (f"Welcome to my page. Listed below are all the available routes for the data.<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
            f"<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(MeasureReference.date, MeasureReference.prcp).filter(MeasureReference.date >= last_year).all()

    # dictionary to hold the query values
    precipitation_dict = {}

    # list to hold the precipiation data
    precipitation_list = []
    
    # grabs the values from the query through a loop
    for date, precipitation in results:
                
        # grabs query data from dictionary via above for loop iterations
        precipitation_dict["date"] = precipitation
        #precipitation_dict["precipitation"] = precipitation

        # appends the grabbed data to the precipitation list
        precipitation_list.append(precipitation_dict)

    # turns the list into a JSON
    #return jsonify(precipitation_list) 
    return {date:prcp for date, prcp in results}


@app.route("/api/v1.0/stations")
def stations():

    # station_results = session.query(MeasureReference.station).all()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    #results = session.query(station.name).all()

    results = session.query(StationReference.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
        
    station_dict = {}

    # list to hold the precipiation data
    station_list = []
    
    #     station_list = session.query(MeasureReference.station, func.count(MeasureReference.station)).\
# group_by(MeasureReference.station).order_by(func.count(MeasureReference.station).desc()).all()
    
#     session.query(MeasureReference.station, func.count(MeasureReference.station)).\
# group_by(MeasureReference.station).all()

    # grabs the values from the query through a loop
    for station in station_results:
                
        # grabs query data from dictionary via above for loop iterations
        station_dict["tobs"] = station
        #precipitation_dict["precipitation"] = precipitation

        # appends the grabbed data to the precipitation list
        station_list.append(station_dict)

    return {station_results}



if __name__ =="__main__":
        app.run(debug=True)
