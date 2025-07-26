import pandas as pd
import os

def load_imdb_data():
    file_path = os.path.join(os.path.dirname(__file__), "movies.csv")  # or imdb_top_1000.csv
    df = pd.read_csv(file_path)

    # Combine fields into a single "text" column for embeddings
    df["text"] = df.apply(
        lambda row: f"{row['Series_Title']} - {row['Genre']} - {row['Overview']}",
        axis=1
    )
    print("the loaded data",df)
    return df
