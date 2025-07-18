import subprocess
from config_manager import Config

class NotificationManager:
    def __init__(self):
        self.config = Config()
        self.notification_config = self.config.get_notification_config()
    
    def send_notification(self, title, message, subtitle="", url=None):
        if not self.notification_config["enabled"]:
            return
        
        title = title.replace('"', '\\"')
        message = message.replace('"', '\\"')
        subtitle = subtitle.replace('"', '\\"')
        
        if url:
            try:
                cmd = [
                    'terminal-notifier',
                    '-title', title,
                    '-message', message,
                    '-open', url,
                    '-timeout', str(self.notification_config["timeout"])
                ]
                if subtitle:
                    cmd.extend(['-subtitle', subtitle])
                if self.notification_config["sound"]:
                    cmd.extend(['-sound', 'default'])
                
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"Notification sent: {title}")
                print(f"Click notification to open: {url}")
                return
                
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("terminal-notifier not found, using AppleScript")
        
        if subtitle:
            applescript = f'display notification "{message}" with title "{title}" subtitle "{subtitle}"'
        else:
            applescript = f'display notification "{message}" with title "{title}"'
        
        if self.notification_config["sound"]:
            applescript += '\nbeep'
        
        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            print(f"Notification sent: {title}")
            if url:
                print(f"URL: {url} (manual open required)")
        except subprocess.CalledProcessError as e:
            print(f"Error sending notification: {e}")
        except FileNotFoundError:
            print("Error: osascript not found. This script only works on macOS.")
