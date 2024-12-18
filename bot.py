import asyncio
import time
from coloredLogs import printWithColor
# from pump_fun import buy, sell
import pandas as pd
import json
# from swap.swap import buy_pump, sell_pumpx
from api.getTokens import fetch_data_from_endpoint, fetch_candlestick_data
from calculations.price import get_current_stats, should_exit_trade, get_current_price, get_current_volume
from calculations.utils import calcualte_percentage_diff, calcualte_volume_percentage_diff
from api.dex_paid import is_dex_paid
from api.getTokenHolders import get_holder_count
from calculations.bondingCurve import (
    filterTokens,
    get_current_bonding_curve_percentage,
)
# from coin_data import get_coin_data
from calculations.entry import (
    calculate_average_price_change,
    calculate_average_volume_change,

    goodEntry,
    calculate_atr,
    calculate_dynamic_tp_sl,
)
from calculations.entry import calculate_current_price_change, calculate_current_volume_change
from trade_settings.settings import settings






# Notes:
# Pump fun fees
# 1% to buy and 1% to sell


# Trade Rules
################################################################
################################################################
################################################################


delta = settings["delta"]
volume_multiplier = settings["volume_multiplier"]
price_multiplier = settings["price_multiplier"]
max_candle_body_multiplier = settings["max_candle_body_multiplier"]
volume_percentage_to_consider = settings["volume_percentage_to_consider"]
sl_coefficient = settings["sl_coefficient"]
rrr = settings["rrr"]

# Take profit settings
min_take_profit = settings["min_take_profit"]
max_take_profit = settings["max_take_profit"]


startingInputAmopunt = settings["startingInputAmopunt"]

# Bonding Curve Thresshold
lowest_bonding_curve = settings["lowest_bonding_curve"]
highest_bonding_curve = settings["highest_bonding_curve"]

#Minimum market cap 
min_market_cap = settings["min_market_cap"]

# Slippage Settings
buy_slippage_percentage = settings["buy_slippage"]
sell_slippage_percentage = settings["sell_slippage"]

buy_priority_fee = settings["buy_priority_in_lamports"]
sell_priority_fee = settings["sell_priority_in_lamports"]

trailing_stop_thresshold = settings["trailing_stop_thresshold"]


################################################################
################################################################
################################################################


# Function to find tokens and calculate bonding curves
async def findTokens(
    delta,
    
    volume_multiplier,
    price_multiplier,
    max_candle_body_multiplier,
    volume_percentage_to_consider,
    sl_coefficient,
    rrr,
    min_take_profit,
    max_take_profit,
):
    while True:
        restart_process = False  # Control flag to restart the whole process

        print(f"Target threshold")
        print(f"--------------------------------")
        print(f"Min Bonding Curve = {lowest_bonding_curve}%")
        print(f"Max Bonding Curve = {highest_bonding_curve}%")
        print(f"Min Market Cap = ${min_market_cap:,}")
        print(f"--------------------------------")

        # Fetch data and bonding curves
        data = await fetch_data_from_endpoint()
        
        
        if data:
            bonding_curves = await filterTokens(
                data, lowest_bonding_curve, highest_bonding_curve, min_market_cap
            )
            
            if not bonding_curves:
                printWithColor(
                    f"No bonding curves found. Waiting 30 seconds before retrying...",
                    "yellow",
                )
                time.sleep(30)
                continue  # Retry the loop
            print("--------------------------------")
            
            # print("--------------------------------")

        selected_bonding_index = 0
        bonding_curves_len = len(bonding_curves)  # Store the length of bonding_curves

        # Create a loop to check entry for each token in the list
        while selected_bonding_index < bonding_curves_len and not restart_process:

            

            
            target_token = bonding_curves[selected_bonding_index]
            target_token_mint = target_token["token_mint"]
            target_token_name = target_token["token_name"]
            target_token_market_cap = target_token["market_cap"]
            target_token_twitter = target_token["twitter"]
            target_token_website = target_token["website"]
            target_token_telegram = target_token["telegram"]

            # holders = await get_holder_count(target_token_mint)
            dex_paid, dex_payment_timestamp = await is_dex_paid(target_token_mint)


            print(f"Current selected index is {selected_bonding_index}")
            print(f"Token:  {target_token_name}")
            print(f"Address:  {target_token_mint}")
            print(f"Market Cap:  ${target_token_market_cap}")
            print(f"Twitter {target_token_twitter}")
            print(f"Website {target_token_website}")
            print(f"Telegram {target_token_telegram}")
            print(f"Is Dex Paid: {dex_paid}")

            




            # Fetch candlestick data and calculate volume/price changes
            candle_stick_data = await fetch_candlestick_data(target_token_mint, 1000, 1)

            

            df = pd.DataFrame(candle_stick_data)

            candle_stick_data_length = len(candle_stick_data)

            # Add the average volume change (removed price change because we don't use it)
            avg_volume_change = calculate_average_volume_change(
                df, volume_percentage_to_consider
            )
            avg_price_change = calculate_average_price_change(df)
            current_volume_change = calculate_current_volume_change(df)
            current_price_change = calculate_current_price_change(df)

            df["body_size"] = abs(df["close"] - df["open"])
            candle_body_size = df["body_size"].iloc[-1]
            period = 14
            avg_body_size = df["body_size"].rolling(window=period).mean()

            tp, sl = calculate_dynamic_tp_sl(
                df.to_dict("records"), delta, sl_coefficient, rrr
            )
            buyPrice, buy_volume, ath = get_current_stats(candle_stick_data)

            entry_good = goodEntry(
                volume_change = current_volume_change,
                price_change = current_price_change,
                avg_volume_change = avg_volume_change,
                avg_price_change = avg_price_change,
                candle_body_size = candle_body_size,
                avg_body_size = avg_body_size,
                candle_stick_data_length =candle_stick_data_length,
                potential_tp = tp,
                volume_multiplier = volume_multiplier,
                price_multiplier = price_multiplier,
                max_candle_body_multiplier = max_candle_body_multiplier,
                min_take_profit = min_take_profit,
                max_take_profit = max_take_profit,
                dex_paid = dex_paid,
            )

            print(f"new entry good or not? {entry_good}")

            print(f"--------------------------------")

            if entry_good:

                printWithColor("Entry Found!")
                # Proceed with the rest of the function since it's a good entry point
                if candle_stick_data:

                    print(
                        f"Current price of {target_token_mint} is {buyPrice} and all-time high is {ath}"
                    )

                   

            else:
                # If it's not a good entry point, increment the index and continue the loop
                selected_bonding_index += 1

                # If we are out of range, exit the loop and restart the outer loop
                if selected_bonding_index == bonding_curves_len:
                    print("Reached the end of the bonding curve list, restarting...")
                    break

        # If a trade was completed, restart the process from the top
        if restart_process:
            continue

        printWithColor(f"No tokens in target threshold", "yellow")
        print(f"Waiting 2 seconds before retrying...")
        time.sleep(2)


# Run the async function
asyncio.run(
    findTokens(
        delta,
        volume_multiplier,
        price_multiplier,
        max_candle_body_multiplier,
        volume_percentage_to_consider,
        sl_coefficient,
        rrr,
        min_take_profit,
        max_take_profit,
    )
)