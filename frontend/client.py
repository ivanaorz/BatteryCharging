import requests
import time

# Defining the base URL for the server
BASE_URL = 'http://127.0.0.1:5000/'

def get_info():
    
    response = requests.get(f'{BASE_URL}info')
    if response.ok:
        info = response.json()
        print(f"Time: {info['sim_time_hour']}:{info['sim_time_min']}")
        print(f"Total Energy Consumption: {info['base_current_load']} kWh")
        print(f"Battery Capacity: {info['battery_capacity_kWh']} kWh")
    else:
        print("Failed to fetch simulation info")


def get_base_load():
    
    print("\n---------Electricity consumption for the household-------------")
    response = requests.get(f'{BASE_URL}baseload')
    if response.ok:
        return response.json()
    else:
        print("Error fetching base load information.")
        return []


def get_price_per_hour():
    
    print("\n---------------Price information for electricity area SE3--------------")
    response = requests.get(f'{BASE_URL}priceperhour')
    if response.ok:
        return response.json()
    else:
        print("Error fetching price per hour information.")
        return []

def get_charge():
    
    try:
        response = requests.get(f'{BASE_URL}charge')
        if response.ok:
            charge_percent = response.json()  
            print(f"Current Battery Charge Level: {charge_percent}%")
            return charge_percent
        else:
            print("Failed to fetch battery charge information.")
            return -1 
    except Exception as e:
        print(f"An error occurred while fetching battery charge status: {e}")
        return -1 

def charge_battery(action):
    """
    Sends a request to start or stop charging the EV battery.
    """
    response = requests.post(f'{BASE_URL}charge', json={'charging': action})
    if response.ok:
        print(f"Charging {'initiated' if action == 'on' else 'concluded'} successfully")
    else:
        print("Failed to send charge command")


def discharge_battery(action):
   
    response = requests.post(f'{BASE_URL}discharge', json={'discharging': action})
   














