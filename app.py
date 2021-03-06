from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import random
import time
import datetime
import math
import pickle
from sklearn.ensemble import RandomForestRegressor
import mysql.connector
import pandas as pd

filename = 'rf_model.sav'
model = pickle.load(open(filename, 'rb'))

db = mysql.connector.connect(
    host='localhost',
    user='gabriel',
    password='password',
    database='hfg_db'
)

app = Flask(__name__)
CORS(app)

@app.route('/all', methods=["GET"])
def all():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM item")
    return_obj = {}
    for row in cursor.fetchall():
        return_obj[row[0]] = {
            "name": row[1],
            "image": row[2],
            "info": row[3],
            "base_price": row[4],
            "wastage": row[5]
        }
    for idx, v in return_obj.items():
        cursor.execute("SELECT * FROM batch WHERE itemid={} ORDER BY expiry ASC LIMIT 1".format(idx))
        row = cursor.fetchall()[0]
        quantity = row[2]
        expiry = row[3]
        price = v['base_price']
        wastage = v['wastage']
        days_expiry = (expiry - datetime.datetime.now()).days + 1
        v['min_price'] = model.predict(np.array([[price, days_expiry, quantity, wastage]])).item()
    return jsonify(return_obj)

@app.route('/item', methods=["GET"])
def single():
    if 'id' in request.args:
        idx = request.args['id']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM item WHERE id={}".format(idx))
        item = cursor.fetchall()[0]
        return_obj = {
            "id": idx,
            "name": item[1],
            "image": item[2],
            "info": item[3],
            "base_price": item[4],
            "discount": []
        }
        price = item[4]
        wastage = item[5]
        cursor.execute("SELECT * FROM batch WHERE itemid={}".format(idx))
        for row in cursor.fetchall():
            quantity = row[2]
            expiry = row[3]
            days_expiry = (expiry - datetime.datetime.now()).days + 1
            return_obj['discount'].append({
                "expiry": expiry,
                "price": model.predict(np.array([[price, days_expiry, quantity, wastage]])).item()
            })
        return jsonify(return_obj)
    else:
        return jsonify({
            "error": "Missing id in request"
        })

if __name__=="__main__":
    #app.run()
    app.run(host="0.0.0.0", port=80)