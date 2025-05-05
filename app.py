from flask import Flask, render_template, request
import pandas as pd
from utils.preprocess import clean_data
from utils.clustering import assign_clusters
from utils.prediction import predict_next_position

import folium
from storm_model import cluster_and_predict

app = Flask(__name__)

@app.route('/')
def index():
    # Đọc dữ liệu đã xử lý
    df = pd.read_csv('data/storms_processed.csv')
    sample_storms = df['SID'].unique()[:5]  # chọn 5 cơn bão đầu
    return render_template('index.html', storm_ids=sample_storms)

@app.route('/map', methods=['POST'])
def show_map():
    storm_id = request.form['storm_id']
    df = pd.read_csv('data/storms_processed.csv')
    storm_df = df[df['SID'] == storm_id]

    if storm_df.empty:
        return "No data for storm ID: " + storm_id

    # Gọi model clustering và random forest
    clustered_df = cluster_and_predict(df, storm_id)

    # Tạo bản đồ Folium
    start_coords = (storm_df.iloc[0]['LAT'], storm_df.iloc[0]['LON'])
    m = folium.Map(location=start_coords, zoom_start=4)

    # Vẽ đường đi thực tế
    for _, row in storm_df.iterrows():
        folium.CircleMarker(
            location=[row['LAT'], row['LON']],
            radius=4,
            color='blue',
            fill=True,
            fill_opacity=0.6,
            popup=f"Wind: {row['USA_WIND']}"
        ).add_to(m)

    # Vẽ đường đi dự đoán
    for _, row in clustered_df.iterrows():
        folium.CircleMarker(
            location=[row['pred_lat'], row['pred_lon']],
            radius=4,
            color='red',
            fill=True,
            fill_opacity=0.6,
            popup=f"Predicted"
        ).add_to(m)

    map_html = m._repr_html_()
    return render_template("index.html", map_html=map_html, storm_ids=df['SID'].unique(), selected=storm_id)



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

