import pandas as pd

pd.read_csv("FORMULATIONS.csv").to_pickle("formulations.pkl")
pd.read_csv("QD32.csv").to_pickle("QD32.pkl")

print("pickle complete!")