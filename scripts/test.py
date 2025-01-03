# https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals?destination=FRPLY&origin=FRMPL&departureDateTime=2025-01-10T01:00:00.000Z
import requests

api_url="https://www.maxjeune-tgvinoui.sncf/api/public/refdata/search-freeplaces-proposals?destination=FRPLY&origin=FRMPL&departureDateTime=2025-01-10T01:00:00.000Z"
response = requests.get(api_url)
print(response)
if response.status_code == 200:
    data = response.json()
    