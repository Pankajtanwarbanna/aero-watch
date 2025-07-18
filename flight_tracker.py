import time
from flight_service import FlightService
from notification_manager import NotificationManager
from config_manager import Config

class FlightTracker:
    def __init__(self, location_key):
        self.config = Config()
        self.location_config = self.config.get_location(location_key)
        
        if not self.location_config:
            raise ValueError(f"Location '{location_key}' not found in configuration")
        
        self.flight_service = FlightService()
        self.notification_manager = NotificationManager()
        self.tracking_config = self.config.get_tracking_config()
        self.seen_planes = set()
        
        self.location_params = {
            "lamin": self.location_config["lamin"],
            "lamax": self.location_config["lamax"],
            "lomin": self.location_config["lomin"],
            "lomax": self.location_config["lomax"]
        }
    
    def start_tracking(self):
        print(f"Starting flight tracking for: {self.location_config['name']}")
        print("Press Ctrl+C to stop")
        
        while True:
            try:
                states = self.flight_service.get_planes_in_area(self.location_params)
                
                for plane in states:
                    icao24 = plane[0]
                    callsign = plane[1].strip() if plane[1] else "Unknown"
                    country = plane[2] or "Unknown"
                    alt = int(plane[7]) if plane[7] else 0
                    
                    if icao24 not in self.seen_planes:
                        self.seen_planes.add(icao24)
                        
                        route = self.flight_service.get_route_info(icao24) or "Route info unavailable"
                        
                        print(f"[NOTIFY] {callsign} | {country} | {alt} m | {route}")
                        
                        adsb_url = f"{self.config.get_setting('adsb_exchange.base_url')}/?icao={icao24}"
                        
                        title = f"✈️ {callsign}"
                        subtitle = f"from {country}"
                        message = f"Altitude: {alt:,} m\nRoute: {route}\n\nClick to view on ADS-B Exchange"
                        
                        self.notification_manager.send_notification(title, message, subtitle, url=adsb_url)
                        break
                        
            except KeyboardInterrupt:
                print("\nStopping flight tracking...")
                break
            except Exception as e:
                print(f"Error in tracking loop: {e}")
            
            time.sleep(self.tracking_config["poll_interval"])
