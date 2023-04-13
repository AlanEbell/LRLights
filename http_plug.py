import requests

# Set the IP address of your Tasmota device
tasmota_ip = "192.168.1.62"

# Set the HTTP API endpoint for toggling the power state
power_toggle_endpoint = f"http://{tasmota_ip}/cm?cmnd=Power%20TOGGLE"

# Send an HTTP GET request to the power toggle endpoint
response = requests.get(power_toggle_endpoint)

# Print the HTTP response status code
print(f"Response status code: {response.status_code}")
