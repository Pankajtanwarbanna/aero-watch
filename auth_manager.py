import requests
import time
from config_manager import Config

class AuthManager:
    def __init__(self):
        self.config = Config()
        self.auth_config = self.config.get_opensky_config()
        self.access_token = None
        self.token_expires_at = 0
    
    def get_access_token(self):
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        print("Getting new access token...")
        
        try:
            response = requests.post(
                self.auth_config["auth_url"],
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.auth_config["client_id"],
                    "client_secret": self.auth_config["client_secret"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                expires_in = token_data.get("expires_in", 1800)
                
                buffer_seconds = self.config.get_setting("tracking.token_buffer_seconds")
                self.token_expires_at = time.time() + expires_in - buffer_seconds
                
                print(f"Access token obtained, expires in {expires_in} seconds")
                return self.access_token
            else:
                print(f"Failed to get access token: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def invalidate_token(self):
        self.access_token = None
        self.token_expires_at = 0
