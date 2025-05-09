from sklearn.ensemble import RandomForestRegressor
import pandas as pd

def predict_next_position(df):
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

    return df[['SID', 'PRED_TIME', 'LAT', 'LON', 'PRED_LAT', 'PRED_LON']]
