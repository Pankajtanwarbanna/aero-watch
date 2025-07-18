import requests
import time
from auth_manager import AuthManager
from config_manager import Config

class FlightService:
    def __init__(self):
        self.config = Config()
        self.auth_manager = AuthManager()
        self.opensky_config = self.config.get_opensky_config()
    
    def get_planes_in_area(self, location_params):
        try:
            url = f"{self.opensky_config['base_url']}/states/all"
            response = requests.get(url, params=location_params, timeout=10)
            data = response.json()
            return data.get("states", [])
        except Exception as e:
            print(f"Error fetching planes: {e}")
            return []
    
    def get_route_info(self, icao24):
        try:
            token = self.auth_manager.get_access_token()
            if not token:
                print("Failed to get access token, skipping route lookup")
                return None
            
            now = int(time.time())
            time_windows = [3600, 7200, 14400, 43200]
            
            for window in time_windows:
                begin_time = now - window
                print(f"Trying route lookup for {icao24} with {window//3600}h window...")
                
                url = f"{self.opensky_config['base_url']}/flights/aircraft"
                response = requests.get(
                    url,
                    params={"icao24": icao24, "begin": begin_time, "end": now},
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10
                )
                
                print(f"API Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    flights = response.json()
                    print(f"Found {len(flights)} flights for {icao24}")
                    
                    if flights:
                        latest = max(flights, key=lambda x: x.get("lastSeen", 0))
                        dep = latest.get("estDepartureAirport") or latest.get("estDepartureAirportHorizDistance")
                        arr = latest.get("estArrivalAirport") or latest.get("estArrivalAirportHorizDistance")
                        
                        if dep and arr:
                            return f"{dep} → {arr}"
                        elif dep:
                            return f"From {dep}"
                        elif arr:
                            return f"To {arr}"
                elif response.status_code == 401:
                    print("Token expired or invalid, will get new token next time")
                    self.auth_manager.invalidate_token()
                    break
                
                time.sleep(1)
            
            return None
            
        except Exception as e:
            print(f"Route fetch error for {icao24}: {e}")
            return None
