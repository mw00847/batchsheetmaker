import PySimpleGUI as sg
from csv_utils import read_csv, write_csv
from helpers import clean_value
from datetime import datetime
import pandas as pd


current_date = datetime.now().strftime('%d-%m-%Y')

def add_to_qd32(product, volume, filled_as=''):
    with open('QD32.csv', 'a', newline='') as file:
        exchequer = ''
        comments = ''
        write_csv('QD32.csv', [[product,volume,current_date]])



def update_dropdown(window, input_text, listbox_key, products):
    matching_products = [product for product in products if input_text.lower() in product.lower()]
    window[listbox_key].update(values=matching_products)

def add_qd32_window():
    global products
    formulations = read_csv('formulations.csv')
    df = pd.DataFrame(formulations).applymap(clean_value)
    products = [row[0] for row in formulations[1:]]

    layout = [[sg.Text("Add QD32", size=(20, 1), justification='center')]]

    for i in range(1, 5):
        layout += [
            [sg.Text(f"Product {i}:"), sg.InputText(key=f'input_text{i}', enable_events=True, expand_x=True)],
            [sg.Listbox(values=[], key=f'product_list{i}', size=(20, 5), enable_events=True, expand_x=True)],
            [sg.Text(f"Volume in L {i}:"), sg.InputText(key=f'volume{i}', expand_x=True)],
            [sg.Text(f"Filled As {i}:"), sg.InputText(key=f'filled_as{i}', expand_x=True)],
        ]

    layout += [[sg.Button("Add"), sg.Button("Back")]]

    window = sg.Window("Add QD32", layout, finalize=True, modal=True)
    window.maximize()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Back":
            break
        if event == "Add":

            for i in range(1, 5):
                selected_products = values.get(f'product_list{i}', [])
                volume = values.get(f'volume{i}')
                filled_as = values.get(f'filled_as{i}')
                if selected_products:
                    product = selected_products[0]
                    if volume:
                        add_to_qd32(product, volume)
                        print(f'Added "{product}" with volume "{volume}" and filled as "{filled_as}" to QD32.csv')
                    window[f'input_text{i}'].update('')
                    window[f'product_list{i}'].update(values=[])
                    window[f'volume{i}'].update('')
                    window[f'filled_as{i}'].update('')
        for i in range(1, 5):
            if event == f'input_text{i}':
                update_dropdown(window, values[f'input_text{i}'], f'product_list{i}', products)

    window.close()
