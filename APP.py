import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

app = Flask(__name__)

------------------------------------------------------------------------------

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        
        f"/api/v1.0/stations<br/>"
        
        f"/api/v1.0/tobs<br/>"
        
        f"/api/v1.0/start<br/>"
      
        f"/api/v1.0/start/end<br/>"
        
    )
    
---------------------------------------------------------------------------------------------    
    
@app.route("/api/v1.0/precipitation")
def precipitation():

    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between
    ('2016-08-23', 'recent')).all()
    date_prcp_df = pd.DataFrame(date_prcp)

    prcp_totals = []
    for result in date_prcp_df:
        row = {}
        row["date"] = date_prcp_df[0]
        row["prcp"] = date_prcp_df[1]
        prcp_totals.append(row)

    return jsonify(prcp_totals)
    
---------------------------------------------------------------------------------------------------

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())
    
---------------------------------------------------------------------------------------------------

@app.route("/api/v1.0/tobs")
def tobs():

    recent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date_prcp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between
    ('2016-08-23', 'recent')).all()
    tobs_prcp_df = pd.DataFrame(date_prcp)

    tobs_totals = []
    for result in temperature:
        row = {}
        row["date"] = tobs_prcp_df[0]
        row["tobs"] = tobs_prcp_df[1]
        tobs_totals.append(row)

    return jsonify(tobs_totals)

----------------------------------------------------------------------------------------------------
    
@app.route("/api/v1.0/<start>")
def trip1(start):


    vacation_start = (2014-9-2)
    vacation_end =  (2014-9-16)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= vacation_start).filter(Measurement.date <= vacation_end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
    
------------------------------------------------------------------------------------------------------

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):


    vacation_start = (2014-9-2)
    data_end =  (2017-8-23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= vacation_start).filter(Measurement.date <= data_end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
    
--------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)
