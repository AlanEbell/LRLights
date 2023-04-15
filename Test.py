import tkinter as tk
import requests

plugs = {'plug1': '192.168.1.62', 'plug2': '192.168.1.68', 'plug3': '192.168.1.70', 'plug4': '192.168.1.71', 'plug5': '192.168.1.72', 'plug6': '192.168.1.73', 'plug7': '192.168.1.74', 'plug8': '192.168.1.75', 'plug9': '192.168.1.76', 'plug10': '192.168.1.77'}

def toggle_power(plug):
    # Set the IP address of your Tasmota device
    tasmota_ip = plugs[plug]

    # Set the HTTP API endpoint for toggling the power state
    power_toggle_endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20TOGGLE"

    # Send an HTTP GET request to the power toggle endpoint
    response = requests.get(power_toggle_endpoint)

    # Print the HTTP response status code
    print(f"Response status code: {response.status_code}")

root = tk.Tk()
root.geometry("800x480")

buttons = {}

for i, plug in enumerate(plugs):
    button = tk.Button(root, text=f"{plug}", width=10, height= 6, bg="light green", command=lambda plug=plug: toggle_power(plug))
    button.grid(row=i//5, column=i%5, padx=5, pady=5)
    buttons[plug] = button

def toggle_all(plug_range):
    for plug in plug_range:
        toggle_power(plug)

toggle1_5 = tk.Button(root, text=f"Toggle all", width=10, height=6, bg="red", command=lambda: toggle_all(['plug1', 'plug2', 'plug3', 'plug4', 'plug5']))
toggle1_5.grid(row=0, column=6, columnspan=5, padx=5, pady=5)

toggle6_10 = tk.Button(root, text=f"Toggle all", width=10, height=6, bg="red", command=lambda: toggle_all(['plug6', 'plug7', 'plug8', 'plug9', 'plug10']))
toggle6_10.grid(row=1, column=6, columnspan=5, padx=5, pady=5)

def toggle_group(plug_range):
    for plug in plug_range:
        toggle_power(plug)

groupbutton = tk.Button(root, text=f"Minimal Living Room", width=15, height=6, bg="light yellow", command=lambda: toggle_group(['plug1', 'plug2', 'plug3']))
groupbutton.grid(row=len(plugs)//5+2, column=1, columnspan=5, padx=5, pady=5)

groupbutton2 = tk.Button(root, text=f"Minimal Living Room 2", width=16, height=6, bg="light yellow", command=lambda: toggle_group(['plug4', 'plug5', 'plug6']))
groupbutton2.grid(row=len(plugs)//5+2, column=4, columnspan=5, padx=5, pady=5)

root.mainloop()
