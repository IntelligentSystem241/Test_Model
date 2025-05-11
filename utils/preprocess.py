def clean_data(df):
    df = df[['SID', 'LAT', 'LON', 'ISO_TIME', 'STORM_SPEED', 'STORM_DIR', 'DIST2LAND']]
    df = df.dropna()
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], format='%m/%d/%Y %H:%M', errors='coerce')
    df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
    df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
    df['STORM_SPEED'] = pd.to_numeric(df['STORM_SPEED'], errors='coerce')
    df['STORM_DIR'] = pd.to_numeric(df['STORM_DIR'], errors='coerce')
    df['DIST2LAND'] = pd.to_numeric(df['DIST2LAND'], errors='coerce')
    df = df.dropna()
    df = df.sort_values(by=['SID', 'ISO_TIME'])
    return df
