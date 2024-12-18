from coloredLogs import printWithColor
import logging

def should_exit_trade(percentage_difference, duration, take_profit, stop_loss, current_bonding_percentage, volume_percentage_difference):
    max_bonding_thresshold = 96
    time_limit = 1800

    if percentage_difference > 0 and volume_percentage_difference <  -10:
        printWithColor("Volume has decreased significantly!", "yellow")
        printWithColor("Potential reversal!", "yellow")
        
        return True, True

    if percentage_difference > take_profit:
        printWithColor(f"Target Hit!", "green")
        logging.info(f"Target Hit! {percentage_difference}")
        
        return True, True
    elif percentage_difference < stop_loss:

        if stop_loss > 0:
            printWithColor("Trailing stop hit!", "green")
            logging.info(f"Trailing Stop Hit! {percentage_difference}")
            return True, True
        else:
            printWithColor("Stop Loss hit!", "red")
            logging.info(f"Stop Loss hit!! {percentage_difference}")
            return True, False
        
    
    elif duration > time_limit:
        printWithColor("Time Hit!", "yellow")
        logging.info(f"Time Hit! Swap at percentage {percentage_difference}")
        logging.info(f"Current Limit {time_limit}")

        return True, False
    
    elif current_bonding_percentage >= max_bonding_thresshold:
        printWithColor("Bonding Curve Hit!", "yellow")
        logging.info(f"Bonding Curve Hit! at percentage {percentage_difference}")

        return True, False
    else:
        return False, False






def get_current_stats(candlestick_data):
    if not candlestick_data:
        return None, None

    # Initialize variables
    all_time_high = float('-inf')
    current_price = None

    for data in candlestick_data:
        # Update all-time high price
        if data['high'] > all_time_high:
            all_time_high = data['high']
        
        # The current price is the latest close price
        # Assuming the data is sorted by timestamp, the last entry is the most recent
        current_price = data['close']
        current_volume = data['volume']
        

    # Calculate the percentage difference
    if all_time_high > 0:
        percentage_difference = ((all_time_high - current_price) / all_time_high) * 100
        print(f"Percentage difference between ATH and current price: {percentage_difference:.2f}%")

    return current_price, current_volume, all_time_high, 




def get_current_price(candlestick_data):
    
    if not candlestick_data:
        printWithColor(f"No candlestick data to get current price", "yellow")
        return None

    current_price = None

    for data in candlestick_data:
        
        # The current price is the latest close price
        # Assuming the data is sorted by timestamp, the last entry is the most recent
        current_price = data['close']


    return current_price



def get_current_volume(candlestick_data):
    
    if not candlestick_data:
        printWithColor(f"No candlestick data to get current price", "yellow")
        return None

    current_price = None

    for data in candlestick_data:
        
        # The current price is the latest close price
        # Assuming the data is sorted by timestamp, the last entry is the most recent
        current_price = data['volume']


    return current_price



def calculate_price(virtual_sol_reserves, virtual_token_reserves):
    price = virtual_sol_reserves / virtual_token_reserves
    return price
        
