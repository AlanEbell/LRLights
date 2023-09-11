import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
from threading import Thread

plugs = {'chair lamp': '192.168.1.62', 'table lamp': '192.168.1.68', 'livingroom 1': '192.168.1.70',
         'livingroom 2': '192.168.1.71', 'piano room': '192.168.1.72', 'piano': '192.168.1.73', 'hallway': '192.168.1.74',
         'plug8': '192.168.1.75', 'plug9': '192.168.1.76', 'plug10': '192.168.1.77'}

buttons = {}


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


def toggle_power(widget, plug):
    tasmota_ip = plugs[plug]
    power_toggle_endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20TOGGLE"
    response = requests.get(power_toggle_endpoint)

    device_state = get_device_state(tasmota_ip)
    if device_state is not None:
        widget.style.background_color = 'lightgreen' if device_state == 'ON' else 'red'


def toggle_group(widget, plug_range):
    for plug in plug_range:
        toggle_power(buttons[plug], plug)


def run_initialize_buttons(widget=None):
    for plug, ip in plugs.items():
        device_state = get_device_state(ip)
        button_color = 'lightgreen' if device_state == 'ON' else 'red' if device_state == 'OFF' else 'gray'

        button = toga.Button(
            plug,
            on_press=lambda widget, plug=plug: toggle_power(widget, plug),
            style=Pack(background_color=button_color)
        )
        buttons[plug] = button
        box.add(button)


def app_startup(widget):
    Thread(target=run_initialize_buttons).start()


# Box
box = toga.Box(
    children=[],
    style=Pack(
        flex=1,
        direction=COLUMN,
        padding=10
    )
)

# Main app
app = toga.App(
    '5th Farm Light Application',
    startup=app_startup,
    main_window=toga.MainWindow(
        title='5th Farm Light Application',
        size=(800, 480)
    )
)

app.main_window.content = box
app.main()
