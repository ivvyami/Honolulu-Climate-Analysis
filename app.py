import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


##############################################
# Database Setup
##############################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)

# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

##########################################
# Flask Setup
##########################################
app = Flask(__name__)



#########################################
# Flask Routes 
#########################################
@app.route("/")
def welcome():
    """List all routes available."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

    @app.route("/api/v1.0/precipitation")
    def percipitation():
        session = Session(engine)

        results = session.query(Measurement.date, func.max(Measurement.prcp)).filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
            group_by(Measurement.date).order_by(Measurement.date).all()

        session.close()
        
        all_percip = []
        for date, prcp in results: 
            percip_dict = {}
            percip_dict["date"] = date
            percip_dict["prcp"] = prcp
            all_percip.append(percip_dict)

        return jsonify(all_percip)

@app.route("/api/v1.0/stations") 
def stations():
    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    station = list(np.ravel(results))

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs(): 
    session = Session(engine)

    sel=[Measurement.station, Measurement.tobs]
    results = session.query(*sel).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    session.close()

    all_tempobs = []
    for station, tobs in results: 
        tempobs_dict = {}
        temp_dict["station"] = station
        temp_dict["tobs"] = tobs
        all_tempobs.append(tempobs_dict)

    return jsonify(all_tempobs)


@app.route("/api/v1.0/<start>")
def start_only():
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >='2011-02-28').all()

    session.close()

    all_start = []
    for tobs[0], tobs[1], tobs[2] in results: 
        start_tobs_dict = {}
        start_tobs_dict["Min"] = tobs[0]
        start_tobs_dict["Avg"] = tobs[1]
        start_tobs_dict["Max"] = tobs[2]
        all_start.append(start_tobs_dict)

    return jsonify(all_start) 

@app.route("/api/v1.0/<start>/<end>")
def start_end(): 
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >='2011-02-28').filter(Measurement.date <= '2011-03-05').all()

    session.close()

    all_start_end = []
    for tobs[0], tobs[1], tobs[2] in results: 
        start_end_tobs_dict = {}
        start_end_tobs_dict["Min"] = tobs[0]
        start_end_tobs_dict["Avg"] = tobs[1]
        start_end_tobs_dict["Max"] = tobs[2]
        all_start_end.append(start_end_tobs_dict)

    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug = True)
















































