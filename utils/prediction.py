from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from flask import request
from datetime import datetime, timedelta

def predict_next_position(df, selected_time_str):
    features = ['LAT', 'LON', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND', 'cluster']
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], errors='coerce')

    X = df[features]
    y_lat = df['LAT'].shift(-1)
    y_lon = df['LON'].shift(-1)
    pred_time = df['ISO_TIME'].shift(-1)

    df = df[:-1].copy()
    X = X[:-1]
    y_lat = y_lat[:-1]
    y_lon = y_lon[:-1]
    pred_time = pred_time[:-1].reset_index(drop=True)

    rf_lat = RandomForestRegressor().fit(X, y_lat)
    rf_lon = RandomForestRegressor().fit(X, y_lon)

    df['PRED_LAT'] = rf_lat.predict(X)
    df['PRED_LON'] = rf_lon.predict(X)
    df['PRED_TIME'] = pred_time

    selected_time = datetime.strptime(selected_time_str, '%Y-%m-%dT%H:%M')
    closest = df.iloc[(df['ISO_TIME'] - selected_time).abs().argsort()[:1]]
    closest['ISO_TIME'] = pd.to_datetime(closest['ISO_TIME']).dt.strftime('%m/%d/%Y %H:%M')

    result = {
        'time': closest['ISO_TIME'].values[0],
        'lat': closest['LAT'].values[0],
        'lon': closest['LON'].values[0],
        'pred_lat': closest['PRED_LAT'].values[0],
        'pred_lon': closest['PRED_LON'].values[0]
    }

    return df[['SID', 'ISO_TIME', 'LAT', 'LON', 'PRED_LAT', 'PRED_LON']]
