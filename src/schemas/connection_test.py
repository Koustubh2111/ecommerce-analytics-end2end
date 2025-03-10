import requests
import time

max_retries = 5
for _ in range(max_retries):
    try:
        response = requests.get("http://schema-registry:8081")
        if response.status_code == 200:
            print("Connection successful!")
            break
    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")
        time.sleep(5)