#!/usr/bin/env python3
import argparse
import sys
from flight_tracker import FlightTracker
from config_manager import Config

def main():
    parser = argparse.ArgumentParser(description='Track flights in specified areas')
    parser.add_argument('location', nargs='?',
                       help='Location to track (blr_airport, hal_area, entire_blr)')
    parser.add_argument('--list-locations', action='store_true',
                       help='List available locations')
    
    args = parser.parse_args()
    
    config = Config()
    
    if args.list_locations:
        print("Available locations:")
        for key, location in config.get_all_locations().items():
            print(f"  {key}: {location['name']}")
        return
    
    if not args.location:
        parser.error("Location is required unless using --list-locations")
    
    try:
        tracker = FlightTracker(args.location)
        tracker.start_tracking()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUse --list-locations to see available options")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nFlight tracking stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
