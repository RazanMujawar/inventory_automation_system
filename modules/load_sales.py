import pandas as pd
def load_sales():
    df=pd.read_csv("data/sales.csv")
    return df