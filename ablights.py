#!/usr/bin/env python3
import tkinter as tk
import requests
import threading
import time

plugs = {'chair lamp': '192.168.1.62', 'table lamp': '192.168.1.68', 'livingroom 1': '192.168.1.70', 'livingroom 2': '192.168.1.71', 'piano room': '192.168.1.72', 'piano': '192.168.1.73', 'hallway': '192.168.1.74', 'plug8': '192.168.1.75', 'plug9': '192.168.1.76', 'plug10': '192.168.1.77'}

# ... (get_device_state and toggle_power functions)

buttons_intialized = False

def run_initialize_buttons():
    initialize_buttons()
    root.after(180000, run_initialize_buttons)  # Reschedule itself




def initialize_buttons():
    

    for i, (plug, ip) in enumerate(plugs.items()):
        device_state = get_device_state(ip)
        if device_state is not None:
            button_color = "light green" if device_state == "ON" else "red"
        else:
            button_color = "gray"

        button = tk.Button(root, text=f"{plug}", width=10, height=6, bg=button_color, command=lambda plug=plug: toggle_power(plug))
        button.grid(row=i // 5, column=i % 5, padx=5, pady=5)
        buttons[plug] = button
    
# ... (rest of the code remains unchanged, except the for loop creating the buttons)

def get_device_state(tasmota_ip):
    url = f'http://{tasmota_ip}/cm?cmnd=Power'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['POWER']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def toggle_power(plug):
    tasmota_ip = plugs[plug]
    power_toggle_endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20TOGGLE"
    response = requests.get(power_toggle_endpoint)

    device_state = get_device_state(tasmota_ip)
    if device_state is not None:
        if device_state == 'ON':
            buttons[plug].config(bg="light green")
        else:
            buttons[plug].config(bg="red")

# ... (rest of the code remains unchanged)


root = tk.Tk()
root.title('5th Farm Light Application')
root.geometry("800x480")

buttons = {}

run_initialize_buttons()

root.after(180000, run_initialize_buttons)  # Time is in milliseconds

def toggle_all(plug_range):
    for plug in plug_range:
        toggle_power(plug)

toggle1_5 = tk.Button(root, text="Toggle all", fg='white', width=10, height=6, bg="black", command=lambda: toggle_all(['chair lamp', 'table lamp', 'livingroom 1', 'livingroom 2', 'piano room']))
toggle1_5.grid(row=0, column=6, columnspan=5, padx=0, pady=0)

toggle6_10 = tk.Button(root, text="Toggle all", fg='white', width=10, height=6, bg="black", command=lambda: toggle_all(['piano', 'hallway', 'plug8', 'plug9', 'plug10']))
toggle6_10.grid(row=1, column=6, columnspan=5, padx=0, pady=0)

def toggle_group(plug_range):
    for plug in plug_range:
        toggle_power(plug)




groupbutton = tk.Button(root, text="Livingroom", width=20, height=6, bg="light blue", command=lambda: toggle_group(['livingroom 1', 'livingroom 2']))
groupbutton.grid(row=3, column=0, sticky='w', columnspan=20, padx=30, pady=0)

groupbutton2 = tk.Button(root, text="Piano Room", width=20, height=6, bg="light blue", command=lambda: toggle_group(['livingroom 2', 'piano room', 'piano']))
groupbutton2.grid(row=3, column=2, sticky='w', columnspan=20, padx=30, pady=0)

groupbutton3 = tk.Button(root, text="Dining Room", width=20, height=6, bg="light blue", command=lambda: toggle_group(['chair lamp', 'table lamp']))
groupbutton3.grid(row=3, column=4, sticky='w', columnspan=20, padx=30, pady=0)




root.mainloop()
