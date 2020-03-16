from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random
import time
import datetime
import math
import pickle
from sklearn.ensemble import RandomForestRegressor

filename = 'rf_model.sav'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
CORS(app)

@app.route('/all', methods=["GET"])
def all():
    return jsonify({
        0: {
            "name": "Milk",
            "image": "image_url",
            "base_price": 5.6,
            "min_price": 2.3
        },
        1: {
            "name": "Halibut",
            "image": "image_url",
            "base_price": 12,
            "min_price": 6
        }
    })

@app.route('/item', methods=["GET"])
def single():
    if 'id' in request.args:
        idx = request.args['id']
        return jsonify({
            "id": idx,
            "name": "Halibut",
            "image": "image_url",
            "info": "Nice fish yum yum",
            "base_price": 12,
            "discount": [
                {
                    "expiry": datetime.datetime.now() + datetime.timedelta(days=1),
                    "price": 6
                },
                {
                    "expiry": datetime.datetime.now() + datetime.timedelta(days=2),
                    "price": 8
                }
            ]
        })
    else:
        return jsonify({
            "error": "Missing id in request"
        })

if __name__=="__main__":
    #app.run()
    app.run(host="0.0.0.0", port=80)