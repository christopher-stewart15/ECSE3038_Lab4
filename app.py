from flask import Flask , request, jsonify,json
from marshmallow import Schema , fields , ValidationError
from json import loads
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
app.config ["SQLALCHEMY_DATABASE_URI"] = "postgres://xnjmrpyj:2juFAqHrzBc9MuVRkVyFIgI7iZZqkKbR@ziggy.db.elephantsql.com:5432/xnjmrpyj"
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


Test_Num = 0


profile_DB = {
    "sucess": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "Christopher Stewart",
        "role": "Electronics Engineer",
        "color": "Blue"
    }
}


class Tank(db.Model):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key = True )
    location = db.Column (db.String (50), unique = True , nullable = False)
    longitude = db.Column (db.String(50), nullable = False)
    latitude = db.Column (db.String(50), nullable = False)
    percentage_full = db.Column (db.Float (), nullable =False)

class TankSchema (ma.SQLAlchemySchema):
    class Meta:
        model = Tank
        fields = ("id","location","longitude","latitude","percentage_full")

db.init_app(app)
migrate = Migrate(app,db)

############################################################
# routes for profile

@app.route("/")
def home():
    return "Welcome to the home page!"

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def profile():
    if request.method == "POST":
       
        profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        profile_DB["data"]["username"] = (request.json["username"])
        profile_DB["data"]["role"] = (request.json["role"])
        profile_DB["data"]["color"] = (request.json["color"])
       
        return jsonify(profile_DB)
   
    elif request.method == "PATCH":
        
        profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        
        x = request.json
        attributes = x.keys()
        
        for attribute in attributes:
            profile_DB["data"][attribute] = x[attribute]
  
        return jsonify(profile_DB)

    else:
        
        return jsonify(profile_DB)


#############################################################################
# routes for tank

@app.route("/tank")
def get_tanks():
    tanks = Tank.query.all()
    tanks_json = TankSchema(many = True).dump(tanks)
    return jsonify(tanks_json)

@app.route("/tank", methods = ["POST"])
def add_tanks():
    newTank = Tank(
        location = request.json["location"],
        longitude = request.json["longitude"],
        latitude = request.json["latitude"],
        percentage_full = request.json["percentage_full"]
    )
    db.session.add(newTank)
    db.session.commit()
    return TankSchema().dump(newTank)

@app.route("/tank/<int:id>", methods = ["PATCH"])
def update_Tank(id):
    tank =Tank.query.get(id)
    update = request.json

    if "location" in update:
        tank.locaton = update["location"]
    if "longitude" in update:
        tank.longitude = update["longitude"]
    if "latitude" in update:
        tank.latitude = update["latitude"]
    if "percentage_full" in update:
        tank.percentage_full = update["percentage_full"]

    db.session.commit()
    return TankSchema().dump(tank)

@app.route("/tank/<int:id>", methods = ["DELETE"])
def delete_tank(id):
    tank =Tank.query.get(id)
    update = request.json
    db.session.delete(tank)
    db.session.commit()

    return {
        "seccess" :True
    }


if __name__ =="__main__" :
    app.run (port=3000, debug = True )