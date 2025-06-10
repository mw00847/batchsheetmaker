import PySimpleGUI as sg
import time


def show_splash():
    layout = [
        [sg.Text("Loading batchsheetmaker", justification='center')],
        [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROG-')],
    ]
    window = sg.Window("Loading", layout, no_titlebar=True, finalize=True, keep_on_top=True)

    for i in range(101):
        time.sleep(0.015)  # simulate loading time
        window['-PROG-'].update(i)
    window.close()
