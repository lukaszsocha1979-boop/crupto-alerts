"""
Crypto Alerts
Birdeye Credits Diagnostic
"""

import requests

from config import BIRDEYE_API_KEY


URL = "https://public-api.birdeye.so/utils/v1/credits"


headers = {
    "X-API-KEY": BIRDEYE_API_KEY,
    "accept": "application/json",
}


print("🚀 Sprawdzam stan CU Birdeye...")

response = requests.get(
    URL,
    headers=headers,
    timeout=20,
)

print()
print("HTTP:", response.status_code)
print("Odpowiedź Birdeye:")
print(response.text)
print()

if response.ok:
    print("✅ Endpoint credits odpowiada.")
else:
    print("❌ Endpoint credits zwrócił błąd.")
