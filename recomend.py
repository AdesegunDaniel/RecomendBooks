from flask import Flask, request, jsonify, render_template, session
import numpy as np
import pandas as pd
import json 
import joblib
import random
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv("model/data.csv")
dataset.set_index('isbn13', inplace=True)
with open("model/categories.json") as file:
    categories = json.load(file)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def ad_home():
    return render_template('rec_home.html')

@app.route('/predict', methods=['POST'])
def predict():
    selected_category = request.form['genre']

    possible_rec = categories[selected_category]
    selected_items = random.sample(possible_rec, 5)
    
    for item in selected_items:
        possible_rec.remove(item)
    
    # Store possible_rec in the session
    session['possible_rec'] = possible_rec

    recomendation = dataset.loc[selected_items]
    recomendation_dict = recomendation.to_dict(orient='records')
    return render_template('rec_result.html', recomendation=recomendation_dict)

@app.route('/recomend', methods=['POST'])
def recomend():
    # Retrieve possible_rec from the session
    possible_rec = session.get('possible_rec', [])

    if len(possible_rec) == 0:
        return render_template('rec_list.html')
    
    elif len(possible_rec) < 5:
        selected_items = possible_rec
        # Remove the selected items from the possible_rec list
        for item in selected_items:
            possible_rec.remove(item)
    else:
        selected_items = random.sample(possible_rec, 5)
    
        for item in selected_items:
            possible_rec.remove(item)

    # Update possible_rec in the session
    session['possible_rec'] = possible_rec

    recomendation = dataset.loc[selected_items]
    recomendation_dict = recomendation.to_dict(orient='records')
    return render_template('rec_result.html', recomendation=recomendation_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=83)
