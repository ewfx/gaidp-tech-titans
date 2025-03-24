import pandas as pd
from sklearn.ensemble import IsolationForest
from multiprocessing import Pool

def detect_anomalies(df_chunk):
    model = IsolationForest(contamination=0.05, random_state=42, n_jobs=1)
    df_chunk["anomaly_score"] = model.fit_predict(df_chunk.select_dtypes(include=['float64', 'int64']))
    return df_chunk

if __name__ == "__main__":
    df_chunks = pd.read_csv("../data/cleaned_data.csv", chunksize=5000)
    
    with Pool(processes=4) as pool:
        results = pool.map(detect_anomalies, df_chunks)

    df_final = pd.concat(results)
    df_final.to_csv("../results/anomalies.csv", index=False)
