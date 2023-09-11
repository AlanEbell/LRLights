import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import RED, GREEN, BLUE, GREY, BLACK, PINK, MAGENTA
import requests

class AndroidLights(toga.App):

    def startup(self):
        print("Starting Class")
         # Create "ALL ON" button
        all_on_button = toga.Button(
            'ALL ON',
            style=Pack(font_family="serif", font_size=10, flex=0, height=75),
            on_press=self.all_on
        )
        all_on_button.style.background_color = GREEN
        
        # Create "ALL OFF" button
        all_off_button = toga.Button(
            'ALL OFF',
            style=Pack(font_family="serif", font_size=10, flex=0, height=75),
            on_press=self.all_off
        )
        all_off_button.style.background_color = MAGENTA
        
        # Add these buttons to your boxes or main layout as you see fit



        self.plugs = {
                        'chair lamp': '192.168.1.62',
                        'table lamp': '192.168.1.68',
                        'livingroom 1': '192.168.1.70',
                        'livingroom 2': '192.168.1.71', 
                        'piano room': '192.168.1.72', 
                        'piano': '192.168.1.73', 
                        'hallway': '192.168.1.74', 
                        'plug8': '192.168.1.75', 
                        'plug9': '192.168.1.76', 
                        'plug10': '192.168.1.77'}

        self.box1 = toga.Box(style=Pack(direction=COLUMN, flex=1))
        self.box2 = toga.Box(style=Pack(direction=COLUMN, flex=1))
                

        self.buttons = {}  # Store button references

        for plug_name in self.plugs.keys():
            button = toga.Button(plug_name,style=Pack(font_family="serif", font_size=10, flex=0, height=75),on_press=self.togglePlug)
                        
            button.style.background_color = GREY
            self.buttons[plug_name] = button  # Save the button reference

            if plug_name in ['chair lamp', 'table lamp', 'livingroom 1','livingroom 2','piano room']:
                self.box2.add(button)
            if plug_name in ['piano','hallway','plug8','plug9','plug10']:
                self.box1.add(button)

        self.box1.add(all_on_button)
        self.box2.add(all_off_button)

        main_box = toga.Box(style=Pack(direction=ROW))
        main_box.add(self.box1)
        main_box.add(self.box2)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        for plug_name, tasmota_ip in self.plugs.items():
            print(plug_name)       
            # Check initial device state and set button color accordingly
            device_state = self.get_device_state(tasmota_ip)
            if device_state == 'ON':
                print(f'device status ON {tasmota_ip}')
                self.buttons[plug_name].style.background_color = GREEN  # Changed to reference the specific button
            if device_state == 'OFF':
                print(f'device status OFF {tasmota_ip}')
                self.buttons[plug_name].style.background_color = RED  # Changed to reference the specific button

            
            


    def togglePlug(self, widget):
        plug_name = widget.text
        tasmota_ip = self.plugs[plug_name]
        endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20TOGGLE"
        
        try:
            response = requests.get(endpoint, timeout=2)  # 2 seconds timeout
            response.raise_for_status()
            device_state = self.get_device_state(tasmota_ip)
            if device_state == 'ON':
                self.buttons[plug_name].style.background_color = GREEN
            else:
                self.buttons[plug_name].style.background_color = RED
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def get_device_state(self, tasmota_ip):
        url = f'http://{tasmota_ip}/cm?cmnd=Power'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['POWER']
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def all_on(self, widget):
        for plug_name, tasmota_ip in self.plugs.items():
            endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20ON"
            try:
                response = requests.get(endpoint)
                response.raise_for_status()
                self.buttons[plug_name].style.background_color = GREEN
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                
    def all_off(self, widget):
        for plug_name, tasmota_ip in self.plugs.items():
            endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20OFF"
            try:
                response = requests.get(endpoint)
                response.raise_for_status()
                self.buttons[plug_name].style.background_color = RED
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")


    

def main():
    print("Starting app")
    return AndroidLights()       



        