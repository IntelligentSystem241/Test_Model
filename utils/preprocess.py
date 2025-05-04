import pandas as pd

def clean_data(df):
    df = df[['SID', 'LAT', 'LON', 'ISO_TIME', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND']]
    df = df.dropna()
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')

    df = df.dropna(subset=['LAT', 'LON'])

    df = df.sort_values(by=['SID', 'ISO_TIME'])
    return df
