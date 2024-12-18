def calculate_trade(
    initial_investment, 
    slippage_percentage, 
    pump_fun_fee, 
    priority_fee, 
    base_transaction_fee,  # Base transaction fee parameter
    exit_fee, 
    take_profit_percentage,
    isBullx=False,  # Boolean flag for Bullx fee
    isPhoton=False  # Boolean flag for Photon fee
):
    # Step 1: Calculate entry amount with slippage
    entry_amount = initial_investment * (1 - slippage_percentage / 100)
    
    # Step 2: Apply the Bullx and Photon fees on the entry amount if the flags are True
    if isBullx:
        entry_amount *= (1 - 0.9 / 100)  # Apply Bullx fee
    if isPhoton:
        entry_amount *= (1 - 1 / 100)  # Apply Photon fee
    
    # Step 3: Calculate the total amount after applying the Pump Fun fee on the buy
    buy_amount_after_fees = entry_amount * (1 - pump_fun_fee / 100)
    
    # Step 4: Calculate the take profit target amount based on the adjusted amount
    take_profit_amount = buy_amount_after_fees * (1 + take_profit_percentage / 100)
    
    # Step 5: Apply the Pump Fun fee on the sell (exit)
    sell_amount_after_pump_fun = take_profit_amount * (1 - pump_fun_fee / 100)
    
    # Step 6: Apply the Bullx and Photon fees on the exit amount if the flags are True
    if isBullx:
        sell_amount_after_pump_fun *= (1 - 0.9 / 100)  # Apply Bullx fee on exit
    if isPhoton:
        sell_amount_after_pump_fun *= (1 - 1 / 100)  # Apply Photon fee on exit
    
    # Step 7: Apply the exit fee to the amount after taking profit
    exit_amount_after_fees = sell_amount_after_pump_fun * (1 - exit_fee / 100)
    
    # Step 8: Calculate the total priority fees and base transaction fees (applied on both buy and sell)
    total_priority_fees = 2 * priority_fee
    total_base_transaction_fees = 2 * base_transaction_fee
    
    # Step 9: Calculate the real PnL after buy and sell fees, including priority fees, base transaction fees, Bullx, and Photon fees
    real_pnl = exit_amount_after_fees - initial_investment - total_priority_fees - total_base_transaction_fees

    # Display results
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Entry Amount (after slippage): ${entry_amount:.2f}")
    print(f"Amount after Buy Fees: ${buy_amount_after_fees:.2f}")
    print(f"Take Profit Target Amount: ${take_profit_amount:.2f}")
    print(f"Amount after Sell Fees: ${sell_amount_after_pump_fun:.2f}")
    print(f"Exit Amount (after all fees): ${exit_amount_after_fees:.2f}")
    print(f"Total Priority Fees: ${total_priority_fees:.2f}")
    print(f"Total Base Transaction Fees: ${total_base_transaction_fees:.2f}")
    print(f"Real PnL after all fees: ${real_pnl:.2f}")

    if real_pnl < 0:
        print(f"To be profitable, you need to increase your take profit to at least: {take_profit_percentage + abs(real_pnl / buy_amount_after_fees * 100):.2f}%")
    else:
        print("Your current take profit percentage is sufficient to be profitable.")

# Example usage with values from your image, including the new Bullx and Photon fees
calculate_trade(
    initial_investment=60,
    slippage_percentage=15,
    pump_fun_fee=1,
    priority_fee=0.5,
    base_transaction_fee=0.5,  # Base transaction fee
    exit_fee=1,
    take_profit_percentage=10,
    isBullx=True,  # Enable Bullx fee
    isPhoton=False  # Enable Photon fee
)



# Settings that this guy has 
# 0.0011
# 0.0005