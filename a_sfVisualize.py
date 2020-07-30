"""
Main file that interacts with the user.
"""

import tkinter as tk
from b_viewCube import ViewCube
from c_wifiInterface import *

"""
0 - network_btn
1 - cube_btn
2 - fusedData_btn
3 - rawData_btn

A button is in ON state if the default task it is mapped to is being executed.
"""
is_btn_on = [False, False, False, False]
stop_threads = False

# Initializing threads
th_view_cube = ViewCube()
th_recv_data = RecvWifiData()
# This instance sends a PING to the server to
# bypass the blocking s.accept() function and stop the server
th_dummy_client = SendWifiData()


def network_btn_clicked():
    global th_recv_data
    global th_dummy_client
    if is_btn_on[0]:
        is_btn_on[0] = False
        if th_recv_data.is_alive():
            th_recv_data.start_server = False
            th_dummy_client.start()
            th_recv_data.join()
            th_dummy_client.join()
        network_btn['text'] = 'Get Data'
        th_dummy_client = SendWifiData()
        th_recv_data = RecvWifiData()
    else:
        if not th_recv_data.is_alive():
            th_recv_data.daemon = True
            if is_btn_on[3]:
                th_recv_data.show_raw_data = True
            th_recv_data.start()
            network_btn['text'] = 'Stop Data'
            is_btn_on[0] = True


def cube_btn_clicked():
    global th_view_cube
    if is_btn_on[1]:
        is_btn_on[1] = False
        if th_view_cube.is_alive():
            th_view_cube.show_cube = False
            th_view_cube.join()
        cube_btn['text'] = 'Open Cube'
        th_view_cube = ViewCube()
    else:
        if not th_view_cube.is_alive():
            th_view_cube.daemon = True
            th_view_cube.start()
            cube_btn['text'] = 'Close Cube'
            th_view_cube.show_cube = True
            is_btn_on[1] = True


def fusedData_btn_clicked():
    if is_btn_on[2]:
        th_recv_data.th_fusion.show_fused_data = False
        fusedData_btn['text'] = 'Show \nFused Data'
        is_btn_on[2] = False
    else:
        fusedData_btn['text'] = 'Hide \nFused Data'
        is_btn_on[2] = True
        th_recv_data.th_fusion.show_fused_data = True
        if is_btn_on[3]:
            rawData_btn_clicked()


def rawData_btn_clicked():
    global th_recv_data
    if is_btn_on[3]:
        th_recv_data.show_raw_data = False
        rawData_btn['text'] = 'Show \nRaw Data'
        is_btn_on[3] = False
    else:
        th_recv_data.show_raw_data = True
        rawData_btn['text'] = 'Hide \nRaw Data'
        is_btn_on[3] = True
        if is_btn_on[2]:
            fusedData_btn_clicked()


def check_cube_closed():
    while not stop_threads:
        if not th_view_cube.is_alive() and th_view_cube.show_cube:
            # the var th_view_cube.show_cube is set to False only by cube_btn_clicked()
            # if the thread is not alive, but the var's var is True, it implies that cube_btn_clicked()
            # was not executed. So, to close the thread, we execute it.
            print('force close cube')
            cube_btn_clicked()


# initialization
if __name__ == '__main__':
    print('Initializing: Sensor Fusion Visualizer')
    # Setting up the window
    window = tk.Tk()
    window.title("Sensor Fusion Visualizer")
    window.geometry("390x380")
    window.resizable(width=False, height=False)
    window.columnconfigure([0, 1], weight=1, minsize=100)
    window.rowconfigure([0, 1], weight=1, minsize=100)

    # Setting up components
    network_btn = tk.Button(master=window, text="Get Data", command=network_btn_clicked)
    network_btn.grid(row=0, column=0, padx=5, pady=5)
    network_btn.config(font=("Calibri", 20))

    cube_btn = tk.Button(master=window, text="Open Cube", command=cube_btn_clicked)
    cube_btn.grid(row=0, column=1, padx=5, pady=5)
    cube_btn.config(font=("Calibri", 20))

    fusedData_btn = tk.Button(master=window, text="Show \nFused Data", command=fusedData_btn_clicked)
    fusedData_btn.grid(row=1, column=0, padx=5, pady=5)
    fusedData_btn.config(font=("Calibri", 20))

    rawData_btn = tk.Button(master=window, text="Show \nRaw Data", command=rawData_btn_clicked)
    rawData_btn.grid(row=1, column=1, padx=5, pady=5)
    rawData_btn.config(font=("Calibri", 20))

    # initializing threads
    th_check_cube = threading.Thread(target=check_cube_closed)
    th_check_cube.daemon = True
    th_check_cube.start()

    window.mainloop()
    print('Program ended gracefully.')
