import PySimpleGUI as sg
from helpers import clean_value, format_float
from csv_utils import read_csv, update_exchequer, add_comments_to_qd32
from pdf_generator import generate_pdf
from datetime import datetime

def view_qd32_window():
    data = read_csv('QD32.csv')
    formulations = read_csv('formulations.csv')

    layout = [
        [sg.Text("View QD32", size=(20, 1), justification='center')],
        [sg.Table(values=data,
                  headings=['Product', 'Volume (L)', 'Date', 'Fill as', 'Exchequer', 'Batch No.', 'Comments'],
                  auto_size_columns=True, num_rows=20, expand_x=True, expand_y=True, enable_events=True, key='table')],
        [sg.Button("Back"), sg.Button("Print Batch Sheets"), sg.Button("Update Exchequer"), sg.Button("Add comments")]
    ]

    window = sg.Window("View QD32", layout, finalize=True, modal=True)
    window.maximize()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Back":
            break

        if event == "Print Batch Sheets":
            selected_rows = values['table']
            if selected_rows:
                selected_product = data[selected_rows[0]][0]
                volume = data[selected_rows[0]][1]

                matching_row = None
                for row in formulations[1:]:
                    if row[0] == selected_product:
                        matching_row = row
                        weight = format_float(float(volume) * float(matching_row[44]))
                        WA = format_float((weight / 100) * float(matching_row[6]))
                        WB = format_float((weight / 100) * float(matching_row[9]))
                        WC = format_float((weight / 100) * float(matching_row[12]))
                        WD = format_float((weight / 100) * float(matching_row[15]))
                        WE = format_float((weight / 100) * float(matching_row[18]))
                        WF = format_float((weight / 100) * float(matching_row[21]))
                        WG = format_float((weight / 100) * float(matching_row[24]))
                        WH = format_float((weight / 100) * float(matching_row[27]))
                        WI = format_float((weight / 100) * float(matching_row[30]))
                        WJ = format_float((weight / 100) * float(matching_row[33]))
                        WK = format_float((weight / 100) * float(matching_row[36]))
                        WL = format_float((weight / 100) * float(matching_row[39]))
                        break

                if matching_row:
                    data_table = [
                        ['A', clean_value(matching_row[6]), WA, clean_value(matching_row[7]), clean_value(matching_row[8]), '', '', ''],
                        ['B', clean_value(matching_row[9]), WB, clean_value(matching_row[10]), clean_value(matching_row[11]), '', '', ''],
                        ['C', clean_value(matching_row[12]), WC, clean_value(matching_row[13]), clean_value(matching_row[14]), '', '', ''],
                        ['D', clean_value(matching_row[15]), WD, clean_value(matching_row[16]), clean_value(matching_row[17]), '', '', ''],
                        ['E', clean_value(matching_row[18]), WE, clean_value(matching_row[19]), clean_value(matching_row[20]), '', '', ''],
                        ['F', clean_value(matching_row[21]), WF, clean_value(matching_row[22]), clean_value(matching_row[23]), '', '', ''],
                        ['G', clean_value(matching_row[24]), WG, clean_value(matching_row[25]), clean_value(matching_row[26]), '', '', ''],
                        ['H', clean_value(matching_row[27]), WH, clean_value(matching_row[28]), clean_value(matching_row[29]), '', '', ''],
                        ['I', clean_value(matching_row[30]), WI, clean_value(matching_row[31]), clean_value(matching_row[32]), '', '', ''],
                        ['J', clean_value(matching_row[33]), WJ, clean_value(matching_row[34]), clean_value(matching_row[35]), '', '', ''],
                        ['K', clean_value(matching_row[36]), WK, clean_value(matching_row[37]), clean_value(matching_row[38]), '', '', ''],
                        ['L', clean_value(matching_row[39]), WL, clean_value(matching_row[40]), clean_value(matching_row[41]), '', '', ''],
                    ]

                    test_headers = ["TEST", "THEORY", "LIMITS", "ACTUAL", "AMENDMENTS"]
                    test_data = [
                        ['SG', matching_row[44], '', '', ''],
                        ['pH', matching_row[46], '', '', ''],
                        ['colour', matching_row[48], '', '', ''],
                        ['others', matching_row[50], '', '', ''],
                    ]

                    current_date = datetime.now().strftime('%d-%m-%Y')
                    generate_pdf(data_table, ['ITEM', '%W/W', 'WEIGHT', 'RAW MATERIAL', 'R#', 'BATCH#', 'CHECK', 'ADDED'],
                                 test_headers, test_data, matching_row, volume, weight, current_date)

        if event == "Update Exchequer":
            selected_rows = values['table']
            if selected_rows:
                update_exchequer(data, selected_rows)
                sg.popup("Exchequer updated.")

        if event == "Add comments":
            selected_rows = values['table']
            if selected_rows:
                comments = sg.popup_get_text("Enter Comments:", "Add Comments")
                if comments:
                    add_comments_to_qd32(data, selected_rows, comments)

    window.close()
