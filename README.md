# Pump Fun Trading Bot

A sophisticated trading bot designed for automated trading on the Pump Fun platform (Solana blockchain). The bot implements advanced strategies for token entry and exit points, with configurable parameters for risk management and profit targeting.

## Overview

This bot monitors tokens on Pump Fun, analyzing various metrics including:
- Bonding curve percentages
- Volume and price changes
- Market cap thresholds
- Token creation time
- DEX payment status
- Trading volume patterns
- Price action indicators

## Key Features

- **Smart Entry Detection**: Analyzes multiple factors including:
  - Volume surge detection
  - Price momentum analysis
  - Bonding curve percentage checks
  - Market cap validation
  - Creation time verification
  - DEX payment status

- **Dynamic Exit Strategy**:
  - Configurable take-profit levels
  - Dynamic stop-loss calculation
  - Volume-based exit triggers
  - Time-based exit conditions
  - Bonding curve threshold monitoring

- **Risk Management**:
  - Customizable slippage settings
  - Priority fee management
  - Dynamic take-profit and stop-loss calculations
  - Volume-based position sizing

## Project Structure

```
├── api/
│   ├── getTokens.py         # Token data fetching from Pump Fun API
│   ├── getTokenHolders.py   # Token holder analysis
│   └── dex_paid.py         # DEX payment verification
├── calculations/
│   ├── bondingCurve.py     # Bonding curve calculations
│   ├── entry.py           # Entry point analysis
│   ├── price.py           # Price calculations and monitoring
│   ├── utils.py           # Utility functions
│   └── creationTime.py    # Token creation time verification
├── trade_settings/
│   └── settings.py        # Trading parameters configuration
├── bot.py                 # Main bot logic
├── pump_fun.py           # Core trading functions
├── pnl_calculator.py     # PnL calculation utilities
└── coloredLogs.py        # Logging utilities
```

## Configuration

The bot's behavior can be customized through the `settings.py` file, which includes:

- Volume multiplier thresholds
- Price multiplier settings
- Candle body size limits
- Take-profit and stop-loss parameters
- Slippage tolerance
- Priority fee settings
- Market cap thresholds
- Bonding curve thresholds

## Trading Strategy

1. **Token Discovery**:
   - Monitors new tokens on Pump Fun
   - Filters based on market cap and creation time
   - Verifies DEX payment status

2. **Entry Analysis**:
   - Checks volume surges against historical averages
   - Analyzes price momentum
   - Validates bonding curve percentages
   - Ensures minimum market cap requirements

3. **Exit Conditions**:
   - Dynamic take-profit based on volatility
   - Trailing stop-loss implementation
   - Volume-based exit triggers
   - Maximum time in trade limits
   - Bonding curve threshold monitoring

## PnL Calculation

The bot includes sophisticated PnL calculation tools that account for:
- Slippage
- Platform fees
- Priority fees
- Transaction costs
- External app fees (optional Bullx/Photon integration)

## Requirements

- Python 3.7+
- Solana blockchain interaction libraries
- Access to Pump Fun API
- Helius API key (for holder analysis)

## Usage

1. Configure your settings in `trade_settings/settings.py`
2. Set up your environment variables (API keys)
3. Run the bot:
```bash
python bot.py
```

## Important Notes

- The bot includes a 1% fee for both buy and sell operations on Pump Fun
- Implements safety checks for token validation
- Includes colored console logging for better monitoring
- Supports integration with external tools (Bullx, Photon)

## Disclaimer

Trading cryptocurrencies involves significant risk. This bot is provided as-is, and users should thoroughly understand its operation before deploying with real funds. 
