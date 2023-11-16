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
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>"
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

        # appends the grabbed data to the precipitation list
        precipitation_list.append(precipitation_dict)

    # turns the list into a JSON
    return {date:prcp for date, prcp in results}

@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(StationReference.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Query the last 12 months of temperature observation data for this station
    results = session.query(MeasureReference.date, MeasureReference.tobs).\
    filter(MeasureReference.date >= last_year).filter(MeasureReference.station == "USC00519281").all()

    tobs_dict = {}

    # list to hold the data
    tobs_list = []
    
    # grabs the values from the query through a loop
    for date, tobs in results:
                
        # grabs query data from dictionary via above for loop iterations
        tobs_dict["date"] = tobs

        # appends the grabbed data to the tobs list
        tobs_list.append(tobs_dict)

    # turns the list into a JSON
    return {date:tobs for date, tobs in results}

@app.route(f"/api/v1.0/<start>")
@app.route(f"/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    
    session = Session(engine)
    
    #select statment
    sel = [func.min(MeasureReference.tobs),
           func.max(MeasureReference.tobs),
           func.avg(MeasureReference.tobs)]
    
    if not end:
    
        start = dt.datetime.strptime(start, "%m%d%Y")
    
        # computes TMIN, TAVG, TMAX for start date
        results = session.query(*sel).\
        filter(MeasureReference.date >= start).all()

        session.close()

        # Converts list of tuples into normal list
        temps = list(np.ravel(results))
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
            filter(MeasureReference.date >= start).\
            filter(MeasureReference.date <= end).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps = temps)


if __name__ =="__main__":
        app.run(debug=True)
