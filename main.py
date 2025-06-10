import PySimpleGUI as sg
from windows_qd32 import view_qd32_window
from windows_add_qd32 import add_qd32_window
from splash_screen import show_splash

def start_window():
    sg.theme('LightGrey1')

    main_layout = [
        [sg.Column([
            [sg.Button("View batches to be made", size=(60, 20)), sg.Button("Calculations", size=(60, 20))],
            [sg.Button("Lab Tests", size=(60, 20)), sg.Button("Add batches", size=(60, 20))]
        ], expand_x=True, expand_y=True, justification='center')]
    ]

    main_window = sg.Window("batchsheetmaker", main_layout, finalize=True)
    #main_window.maximize()

    while True:
        event, _ = main_window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "View batches to be made":
            view_qd32_window()
        elif event == "Add batches":
            add_qd32_window()


    main_window.close()

if __name__ == "__main__":
    show_splash()
    start_window()
