from sklearn.ensemble import RandomForestRegressor

def predict_next_position(df):
    features = ['LAT', 'LON', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND', 'cluster']
    X = df[features]
    y_lat = df['LAT'].shift(-1)
    y_lon = df['LON'].shift(-1)

    df = df[:-1]
    X = X[:-1]
    y_lat = y_lat[:-1]
    y_lon = y_lon[:-1]

    rf_lat = RandomForestRegressor().fit(X, y_lat)
    rf_lon = RandomForestRegressor().fit(X, y_lon)

    df['PRED_LAT'] = rf_lat.predict(X)
    df['PRED_LON'] = rf_lon.predict(X)
    return df[['SID','ISO_TIME', 'LAT', 'LON', 'PRED_LAT', 'PRED_LON']]
