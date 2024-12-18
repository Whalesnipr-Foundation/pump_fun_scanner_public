import requests
import json
from dotenv import load_dotenv
import os
import asyncio 

load_dotenv()

api_key = os.getenv("HELIUS_API_KEY")

# Replace <api_key> with your actual Helius API key
url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"

async def get_holder_count(mint):
    all_owners = set()
    cursor = None
    mint_address = mint
    
    while True:
        # Define the parameters for the request
        params = {
            "limit": 1000,
            "mint": mint_address
        }

        # Add cursor to params if it exists (for pagination)
        if cursor:
            params["cursor"] = cursor

        # Make the request to the Helius API
        response = requests.post(url, json={
            "jsonrpc": "2.0",
            "id": "helius-test",
            "method": "getTokenAccounts",
            "params": params
        }, headers={
            "Content-Type": "application/json"
        })

        # Parse the response JSON
        data = response.json()

        # Check if there are token accounts in the response
        if not data.get("result") or not data["result"].get("token_accounts"):
            print("No more results")
            break

        # Extract the owner addresses and add them to the set
        for account in data["result"]["token_accounts"]:
            all_owners.add(account["owner"])

        # Update the cursor for the next batch
        cursor = data["result"].get("cursor")
        if not cursor:
            break
    

    unique_holders = len(all_owners)
    # Print the number of unique owners
    # print(f"Number of unique holders: {unique_holders}")





    return unique_holders



asyncio.run(get_holder_count("FCJQjmjmNXphDG7nL4ax3Ya68THxdv6gd3vJYeFYpump"))