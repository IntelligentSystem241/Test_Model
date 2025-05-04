from sklearn.cluster import KMeans

def assign_clusters(df, n_clusters=5):
    df['cluster'] = KMeans(n_clusters=n_clusters, random_state=42).fit_predict(df[['LAT', 'LON']])
    return df
