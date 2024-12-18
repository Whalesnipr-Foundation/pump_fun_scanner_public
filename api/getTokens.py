
import requests
import asyncio

async def fetch_data_from_endpoint():
    url = "https://frontend-api.pump.fun/coins/for-you"
    params = {
        "offset": 0,
        "limit": 50,
        "includeNsfw": "false"
    }
    
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        
        return response_json
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None



async def token_overview(address,):
    url = f"https://frontend-api.pump.fun/coins/{address}"
    
    
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        
        return response_json
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


async def fetch_candlestick_data(address, limit, timeframe):
    # Define the URL and parameters
    url = f"https://frontend-api.pump.fun/candlesticks/{address}"
    params = {
        "offset": 0,
        "limit": {limit},
        "timeframe": {timeframe}
    } 
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # print(f"candlestick data {response.json()}")    
            return response.json()  # Return the JSON response
        
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None