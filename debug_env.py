import os
from dotenv import load_dotenv

print("--- AVANT load_dotenv ---")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

load_dotenv(override=True)
print("\n--- APRES load_dotenv(override=True) ---")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
