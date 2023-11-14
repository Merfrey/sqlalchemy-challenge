# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
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
    
    #grabs the values from the query through a loop
    for date, precipitation in results:
                
        #grabs query data from dictionary via above for loop iterations
        precipitation_dict["date"] = precipitation
       # precipitation_dict["precipitation"] = precipitation

        #appends the grabbed data into the precipitation list
        precipitation_list.append(precipitation_dict)

        #turns the list into a JSON
    return jsonify(precipitation_list) 
    
#     for x in session.query(sortedRain).all():
#         print(x.__dict__)
    
#     return {date:prcp for date, prcp in sortedRain}


if __name__ =="__main__":
        app.run(debug=True)
