import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path(__file__).parent / "config"
        self._locations = self._load_json("locations.json")
        self._settings = self._load_json("settings.json")
    
    def _load_json(self, filename):
        with open(self.config_dir / filename, 'r') as f:
            return json.load(f)
    
    def get_location(self, location_key):
        return self._locations.get(location_key)
    
    def get_all_locations(self):
        return self._locations
    
    def get_setting(self, key_path):
        keys = key_path.split('.')
        value = self._settings
        for key in keys:
            value = value.get(key)
            if value is None:
                return None
        return value
    
    def get_opensky_config(self):
        return self._settings["opensky"]
    
    def get_tracking_config(self):
        return self._settings["tracking"]
    
    def get_notification_config(self):
        return self._settings["notifications"]
