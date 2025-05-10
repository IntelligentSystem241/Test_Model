from flask import Flask, render_template, request
import pandas as pd
from utils.preprocess import clean_data
from utils.clustering import assign_clusters
from utils.prediction import predict_next_position



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('training4.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['storm_file']
    df = pd.read_csv(file, skiprows=[1], low_memory=False)
    df_clean = clean_data(df)
    df_clustered = assign_clusters(df_clean)
    selected_time_str = request.form['selected_time']
    predictions = predict_next_position(df_clustered, selected_time_str)

    return render_template('training4.html', predictions=predictions.to_dict(orient='records'))

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sẽ đặt biến PORT
    app.run(host="0.0.0.0", port=port)
