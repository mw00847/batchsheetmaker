import csv
import pandas as pd
from datetime import datetime

def read_csv(filename):
    df = pd.read_csv(filename)
    return df.values.tolist()

def write_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def update_exchequer(data, selected_rows):
    updated_data = data.copy()
    current_date = datetime.now().strftime('%d-%m-%Y')
    for row in selected_rows:
        while len(updated_data[row]) < 7:
            updated_data[row].append('')
        updated_data[row][4] = f"added ({current_date})"
    pd.DataFrame(updated_data).to_csv('QD32.csv', index=False)

def add_comments_to_qd32(data, selected_rows, comments):
    updated_data = data.copy()
    for row in selected_rows:
        while len(updated_data[row]) < 7:
            updated_data[row].append('')
        updated_data[row][6] = comments
    pd.DataFrame(updated_data).to_csv('QD32.csv', index=False)




