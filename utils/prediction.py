from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from flask import request
from datetime import datetime, timedelta

def predict_next_position(df, selected_time_str):
    features = ['LAT', 'LON', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND', 'cluster']

    # Đảm bảo ISO_TIME là kiểu datetime
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], errors='coerce')

    # Dịch dữ liệu một bước để tạo nhãn dự đoán
    X = df[features]
    y_lat = df['LAT'].shift(-1)
    y_lon = df['LON'].shift(-1)
    pred_time = df['ISO_TIME'].shift(-1)

    # Cắt bỏ dòng cuối (vì sau shift sẽ chứa NaN / NaT)
    df = df[:-1].copy()
    X = X[:-1]
    y_lat = y_lat[:-1]
    y_lon = y_lon[:-1]
    pred_time = pred_time[:-1].reset_index(drop=True)

    # Huấn luyện mô hình
    rf_lat = RandomForestRegressor().fit(X, y_lat)
    rf_lon = RandomForestRegressor().fit(X, y_lon)

    # Gán kết quả dự đoán
    df['PRED_LAT'] = rf_lat.predict(X)
    df['PRED_LON'] = rf_lon.predict(X)
    df['PRED_TIME'] = pred_time

    selected_time_str = request.form['selected_time']
    selected_time = datetime.strptime(selected_time_str, '%m/%d/%Y %H:%M')

    # Tìm hàng gần nhất (có thể dùng khoảng ±1 giờ hoặc chính xác)
    closest = storm_data.iloc[(storm_data['ISO_TIME'] - selected_time).abs().argsort()[:1]]
    result = {
        'time': closest['ISO_TIME'].values[0],
        'lat': closest['LAT'].values[0],
        'lon': closest['LON'].values[0],
        'pred_lat': closest['PRED_LAT'].values[0],
        'pred_lon': closest['PRED_LON'].values[0]
    }
    return df[['SID', 'PRED_TIME', 'LAT', 'LON', 'PRED_LAT', 'PRED_LON']]
