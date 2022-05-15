import sqlite3
import os
import statistics

from flask import Flask, request, render_template


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('fission.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('home.html', message="Enter a zipcode")

@app.route('/', methods=['POST'])
def index_post():

    zipcode = int(request.form['text'])

    conn = get_db_connection()
    query = (
        "SELECT pricing.price, pricing.area, "
               "features.bed, features.bath, "
               "address, city, zipcode FROM location "
        "INNER JOIN pricing USING (id) "
        "INNER JOIN features USING (id) "
        f"WHERE zipcode = {zipcode} "
        "LIMIT 10;"
    )
    posts = conn.execute(query).fetchall()
    conn.close()
    
    
    if len(posts) < 1:
        return render_template('home.html', message="No listings in that zipcode")

    prices = []
    for listing in posts:
        prices.append(listing['price'])
    
    prices.sort()
    stats_dict = {
        "low" : prices[0],
        "high" : prices[-1],
        "mean" : statistics.mean(prices),
        "std" : statistics.stdev(prices) // 1
    }

    return render_template('loop.html', listings=posts, stats=stats_dict)