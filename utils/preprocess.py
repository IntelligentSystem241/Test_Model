import pandas as pd

def clean_data(df):
    df = df[['SID', 'LAT', 'LON', 'ISO_TIME', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND']]
    df = df.dropna()
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], errors='coerce')
    df = df.sort_values(by=['SID', 'ISO_TIME'])
    return df
