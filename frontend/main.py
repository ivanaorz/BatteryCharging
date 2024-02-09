from client import get_info, get_base_load, get_price_per_hour, charge_battery, discharge_battery, get_charge
import time

def find_optimal_charging_hours(prices, consumption):
    """
    Finding the hours with the lowest electricity prices and consumption.
    """
    combined = [(price + cons, hour) for hour, (price, cons) in enumerate(zip(prices, consumption))]
    sorted_hours = sorted(combined, key=lambda x: x[0])
    optimal_hours = [hour for _, hour in sorted_hours[:len(sorted_hours)//3]]
    return optimal_hours

def prompt_user():
    response = input("Do you want to start charging the battery? yes/no: ").strip().lower()
    return response == 'yes'

def format_hour(hour):
    
    return f"{hour:02d}:00"

def main():
    continue_charging = prompt_user()
    while continue_charging:
        discharge_battery("on")
        time.sleep(1)  # Allowing time for discharge command to take effect

        prices = get_price_per_hour()
        for hour, price in enumerate(prices):
            print(f"Hour {hour}: {price} öre/kWh")

        base_load = get_base_load()
        for hour, load in enumerate(base_load):
            print(f"Hour {hour}: {load} kWh")
        optimal_hours = find_optimal_charging_hours(prices, base_load)
        print(f"\n Optimal charging hours based on low prices and consumption: {optimal_hours}")

        charging_started = False
        for current_hour in range(24):  
            actual_time = format_hour(current_hour)  
            print(f"\n------{actual_time}------")

            if current_hour in optimal_hours:
                if not charging_started:
                    print("Starting charging process based on optimal conditions...")
                    charge_battery("on")
                    charging_started = True
            else:
                if charging_started:
                    print("Stopping charging due to non-optimal hour.")
                    charge_battery("off")
                    charging_started = False
                continue 

            charge_status = get_charge()

            if charge_status != -1:
                print(f"Price for this hour: {prices[current_hour]} öre/kWh")
                print(f"Household base load for this hour: {base_load[current_hour]} kWh")
                get_info()

            

            if charge_status >= 80:
                print("Battery reached 80%. Stopping the charging process.")
                charge_battery("off")
                discharge_battery("on")
                time.sleep(4)
                break  # Breaking out of the loop once charged to 80%

            elif charge_status == -1:
                print("Failed to fetch the current charging status, skipping this hour.")

            time.sleep(4)  # Simulating an hour passing in real-time as 4 seconds in the simulation

        
        print("Completed a full day cycle.")
        continue_charging = prompt_user()
        if continue_charging:
            print("Restarting the cycle for the next day as per user request.")
        else:
            print("Ending the simulation as per user choice.")
            break 

if __name__ == "__main__":
    main()
    
        





    