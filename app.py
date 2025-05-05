from flask import Flask, render_template, request
import pandas as pd
from utils.preprocess import clean_data
from utils.clustering import assign_clusters
from utils.prediction import predict_next_position



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['storm_file']
    df = pd.read_csv(file)

    df_clean = clean_data(df)
    df_clustered = assign_clusters(df_clean)
    predictions = predict_next_position(df_clustered)

    return render_template('result.html', predictions=predictions.to_dict(orient='records'))

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sẽ đặt biến PORT
    app.run(host="0.0.0.0", port=port)

