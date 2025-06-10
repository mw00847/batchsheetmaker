import pandas as pd

def clean_value(val):
    if pd.isna(val) or str(val).lower() == 'nan':
        return ' '
    return val

def format_float(value, precision=2):
    return round(value, precision)
