import json
import numpy as np
import pandas as pd
from coloredLogs import printWithColor


def goodEntry(
    volume_change,
    price_change,
    avg_volume_change,
    avg_price_change,
    candle_body_size,
    avg_body_size,
    candle_stick_data_length,
    potential_tp,
    volume_multiplier,
    price_multiplier,
    max_candle_body_multiplier,
    min_take_profit,
    max_take_profit,
    dex_paid

):

    # Dynamic thresholds based on averages and multipliers
    dynamic_volume_threshold = avg_volume_change * volume_multiplier
    dynamic_price_threshold = avg_price_change * price_multiplier
    
    if not dex_paid:
        printWithColor("DEX not paid, skipping entry", "yellow")
        return False


    if potential_tp < min_take_profit or potential_tp > max_take_profit:
        printWithColor(f"Potential TP {potential_tp} too low or too high", "yellow")
        return False

    if candle_stick_data_length < 20:
        printWithColor(f"Not enough candle data to consider trading: {candle_stick_data_length}", "yellow")
        return False
   
    latest_avg_body_size = avg_body_size.iloc[-1]

    # Avoid entering on large candles (too volatile)
    if candle_body_size > latest_avg_body_size * max_candle_body_multiplier:
        printWithColor(f"Candle too large", "yellow")
        return False

    # Avoid entering during strong negative price and volume changes (heavy sell pressure)
    if volume_change < 0 and price_change < 0:
        return False

    # Ensure price change is positive and exceeds the dynamic price threshold (sign of new money coming in)
    if price_change > dynamic_price_threshold:
        # Check for volume surge (early momentum) above the dynamic volume threshold
        if volume_change > dynamic_volume_threshold:
            # Allow larger price changes by loosening ATR filter

            return True  # Good entry point
    else:
        printWithColor(f"Volume or price not above thresshold", "yellow")
        
    
    return False


def calculate_average_price_change(df):
    price_changes = []
    for i in range(1, len(df)):
        previous_price = df['close'][i - 1]
        current_price = df['close'][i]
        if previous_price == 0:
            continue
        price_change = ((current_price - previous_price) / previous_price) * 100
        price_changes.append(price_change)
    return np.mean(price_changes)


# This function calculates the Average True Range (ATR) for a given DataFrame `df` of OHLC (Open, High, Low, Close) data.
# The ATR is a measure of market volatility, and it gives insight into how much price typically moves during a given period.
#
# Steps:
# 1. Calculate the 'high-low' range, which is the difference between the high and low prices of each candle.
# 2. Calculate the 'high-prev-close', which is the absolute difference between the high of the current candle and the close of the previous candle.
# 3. Calculate the 'low-prev-close', which is the absolute difference between the low of the current candle and the close of the previous candle.
# 4. Create a new column 'true_range', which is the maximum of the three calculated values ('high-low', 'high-prev-close', 'low-prev-close') for each row.
#    This represents the largest price movement between the high, low, and previous close.
# 5. Calculate the Average True Range (ATR) by applying a rolling mean over the 'true_range' column, using a specified window size (default 14 periods).
# 6. The
def calculate_atr(df, period=14):
    df['high-low'] = df['high'] - df['low']
    df['high-prev-close'] = abs(df['high'] - df['close'].shift(1))
    df['low-prev-close'] = abs(df['low'] - df['close'].shift(1))
    df['true_range'] = df[['high-low', 'high-prev-close', 'low-prev-close']].max(axis=1)
    df['atr'] = df['true_range'].rolling(window=period).mean()
    return df['atr']


# This function calculates the average percentage change in trading volume between consecutive candles in a DataFrame `df` containing OHLCV data.
# The purpose is to measure the average rate at which volume is increasing or decreasing over time.
#
# Steps:
# 1. Initialize an empty list `volume_changes` to store the percentage change in volume between consecutive candles.
# 2. Loop through the DataFrame starting from the second row (index 1), and for each candle:
#    - Extract the `previous_volume` from the prior candle.
#    - Extract the `current_volume` from the current candle.
# 3. If the `previous_volume` is 0, skip that iteration to avoid division by zero.
# 4. Calculate the percentage change in volume between the current and previous candles using the formula:
#    ((current_volume - previous_volume) / previous_volume) * 100
# 5. Append the calculated `volume_change` to the `volume_changes` list.
# 6. After the loop, return the average of the values in the `volume_changes` list using `np.mean`.
#    This represents the average percentage change in trading volume over the period.


def calculate_average_volume_change(df, percentage):
    # Calculate how many candles make up the nearest 20% of the data
    num_candles = int(len(df) * percentage)
    
    # Filter the dataframe for the most recent 20% of the data
    recent_df = df.tail(num_candles)
    
    # Initialize an empty list to store the volume changes
    volume_changes = []
    
    # Calculate percentage volume changes for the recent candles
    for i in range(1, len(recent_df)):
        previous_volume = recent_df['volume'].iloc[i - 1]
        current_volume = recent_df['volume'].iloc[i]
        
        # Ensure we're not dividing by zero
        if previous_volume == 0:
            continue
        
        # Calculate the percentage change in volume
        volume_change = ((current_volume - previous_volume) / previous_volume) * 100
        volume_changes.append(volume_change)
    
    # Return the average volume change over the most recent 20% of data
    return np.mean(volume_changes) if volume_changes else 0


# This function calculates dynamic Take Profit (TP) and Stop Loss (SL) percentages based on recent candlestick data,
# volatility (price range), and a given risk-to-reward ratio (RRR). The SL is adjusted by a coefficient, and TP is derived
# based on the SL and RRR.
#
# Parameters:
# - `candlestick_data`: A list of candlestick data, where each entry contains OHLC (Open, High, Low, Close) values.
# - `delta`: The number of recent candles to consider when calculating TP and SL.
# - `sl_coefficient`: A multiplier applied to the calculated stop loss, adjusting the SL based on risk preference.
# - `rrr`: The risk-to-reward ratio (default is 2), which determines how much reward (profit) is sought for a given risk.
#
# Steps:
# 1. Extract the last `delta` number of candles from the provided `candlestick_data` to work with recent data.
# 2. Collect the `high`, `low`, and `close` values from these recent candles.
# 3. Calculate the average range over the selected period (`delta`), which is the total range between highs and lows divided by `delta`.
# 4. Get the `current_price`, which is the most recent close price from the extracted data.
# 5. Calculate the stop loss (SL) percentage:
#    - The stop loss is based on the average range relative to the current price, multiplied by the `sl_coefficient`.
#    - Add an additional 5% buffer to the stop loss to account for market volatility.
# 6. Calculate the take profit (TP) percentage:
#    - The TP is derived by multiplying the stop loss by the risk-to-reward ratio (`rrr`), aiming for a reward that is `rrr` times the risk.
# 7. Return the calculated `take_profit_percentage` and the negative `stop_loss_percentage`, which represent dynamic TP and SL values.

def calculate_dynamic_tp_sl(candlestick_data, delta, sl_coefficient, rrr):
    recent_candles = candlestick_data[-delta:]
    highs = [candle['high'] for candle in recent_candles]
    lows = [candle['low'] for candle in recent_candles]
    closes = [candle['close'] for candle in recent_candles]
    
    avg_range = (sum(highs) - sum(lows)) / delta
    current_price = closes[-1]
    
    stop_loss_percentage = (avg_range / current_price) * 100 * sl_coefficient
    stop_loss_percentage += 5

    take_profit_percentage = stop_loss_percentage * rrr
    
    return take_profit_percentage, -stop_loss_percentage


def calculate_current_volume_change(df):
    # Ensure there are at least two rows to compare
    if len(df) < 2:
        raise ValueError("DataFrame must contain at least two rows to calculate volume change.")
    
    # Get the volume for the most recent row and the previous row
    last_volume = df['volume'].iloc[-1]      # Volume of the last row
    previous_volume = df['volume'].iloc[-2]  # Volume of the second-to-last row

    # Calculate percentage volume change
    if previous_volume == 0:
        return 0  # Avoid division by zero if previous volume is zero
    volume_change = ((last_volume - previous_volume) / previous_volume) * 100

    printWithColor(f"Current volume change {volume_change}", "info")

    return volume_change


def calculate_current_price_change(df):
    for i in range(1, len(df)):
        price_change = ((df['close'][i] - df['close'][i - 1]) / df['close'][i - 1]) * 100

        
    printWithColor(f"Current price change {price_change}", "info")

    return price_change
