import pandas as pd
import numpy as np
from numba import jit
from sklearn.preprocessing import StandardScaler

def load_data(file_path, chunksize=10000):
    return pd.read_csv(file_path, chunksize=chunksize)

@jit(nopython=True)
def clean_text(value):
    return value.strip() if isinstance(value, str) else value

def preprocess_data(df):
    df.fillna("UNKNOWN", inplace=True)
    df = df.applymap(clean_text)
    scaler = StandardScaler()
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

if __name__ == "__main__":
    processed_chunks = []
    for chunk in load_data("../data/regulatory_dataset.csv"):
        processed_chunk = preprocess_data(chunk)
        processed_chunks.append(processed_chunk)

    df_final = pd.concat(processed_chunks)
    df_final.to_csv("../data/cleaned_data.csv", index=False)
