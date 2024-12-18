from solana.rpc.api import Client
from solders.keypair import Keypair #type: ignore
import dotenv
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()




# PRIV_KEY = "YOUR_PRIVATE"
RPC = "RPC"
client = Client(RPC)
# payer_keypair = Keypair.from_base58_string(PRIV_KEY)
