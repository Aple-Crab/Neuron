from flask import Flask, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client
from dotenv import load_dotenv, dotenv_values
load_dotenv()

app = Flask(__name__)
CORS(app)

url = os.getenv("URL")
key = os.getenv("SECRET_KEY")
supabase = create_client(url, key)

@app.route("/geoports", methods=["GET"])
def get_geodata():
    try:
        data = supabase.table('geoports').select('name, lat, long', 'geom').execute()

        datalist = []
        for objectlist in data:
            for row in objectlist:
                if str(type(row)) == "<class 'list'>":
                    datalist.append(row)
                else:
                    continue

        features = []      
        for objects in datalist:
            for row in objects:
                # print(row)
                geometry = row["geom"]
                feature = {
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": {
                    'name': row["name"].replace('"', "'"),
                    'latitude': row["lat"],
                    'longitude': row["long"]
                    }
                }
                features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        return jsonify(feature_collection)

    except Exception as e:
        return {'Geoports API error': str(e)}
    
    
@app.route("/geodata", methods=["GET"])
def get_geoports():
    try:
        data = supabase.table('geodata').select('name, lat, long', 'heading', 'time', 'geom').execute()

        datalist = []
        for objectlist in data:
            for row in objectlist:
                if str(type(row)) == "<class 'list'>":
                    datalist.append(row)
                else:
                    continue

        features = []      
        for objects in datalist:
            for row in objects:
                # print(row)
                geometry = row["geom"]
                feature = {
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": {
                    'name': row["name"].replace('"', "'"),
                    'latitude': row["lat"],
                    'longitude': row["long"],
                    'heading': row["heading"],
                    'time': row["time"],
                    }
                }
                features.append(feature)

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }

        return jsonify(feature_collection)

    except Exception as e:
        return {'Geodata API error': str(e)}


@app.route("/frequency", methods=["GET"])
def get_ship_visits():
    try:
        data = supabase.table('frequency').select('ship_name', 'port_name').execute()

        datalist = []
        for objectlist in data:
            for row in objectlist:
                if str(type(row)) == "<class 'list'>":
                    datalist.append(row)
                else:
                    continue

        features = []      
        for objects in datalist:
            for row in objects:
                feature = {
                    'name': row["ship_name"].replace("ship_", "Ship "),
                    'ports': row["port_name"].split(" + "),
                }
                features.append(feature)


        return jsonify(features)

    except Exception as e:
        return {'Frequency API error': str(e)}


if __name__ == '__main__':
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))