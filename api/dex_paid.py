import requests
import asyncio
import json
from coloredLogs import printWithColor



async def is_dex_paid(token_address):
   

    # URL for the GET request
    url = f"https://api.dexscreener.com/v1/orders/solana/{token_address}"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response to JSON
        data = response.json()
        print(data)
    
        if data:
            type = data[0].get('type')
            if type == 'tokenProfile':

                status = data[0].get('status')
                paymentTimestamp = data[0].get('paymentTimestamp')
                print(f"dex paid timeststamp {paymentTimestamp}")
                print(f'status: {status}')

                if status == 'approved':
                    printWithColor('Dex Paid!', "green")
                    return True, paymentTimestamp
                else:
                    printWithColor("Dex Not Paid!", "red")
                    return False, 0
        else:
            print("Dex info not found!", "yellow")
            return False, 0  
        
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return False, 0


asyncio.run(is_dex_paid("YmHQjqxwdaZP6p1nMJzVuCAZ592vAjyH8FRM5Gypump"))
