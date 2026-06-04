import pandas as pd
def load_sales(file_path):
    df=pd.read_csv("data/sales.csv")
    return df