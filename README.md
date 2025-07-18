# Aero Watch ✈️

My desk at [InMobi](https://www.inmobi.com/) is right next to a window, and I get a clear view of planes flying around HAL Airport. I built a tool that sends me a little notification whenever one flies by - with flight details and route information.

Flight data is publicly broadcasted through ADS-B signals and you can even see it live on sites like [ADSB Exchange](https://globe.adsbexchange.com). So I tapped into it and added a personal touch.

Now, every time a plane passes, my system goes: *"Hey, look up!"* with all the flight details. Sometimes it's a private charter, sometimes a training flight, and once it was an old air force jet.

Kind of like birdwatching, but for planes. 🛬

**This project went viral on Twitter:** [Check out the original post](https://x.com/the2ndfloorguy/status/1945750355096310213)

## Features

- Track flights in your area (BLR Airport, HAL Area, or entire Bangalore)
- Real-time macOS notifications with route information  
- Click notifications to view aircraft on ADSB Exchange
- Modular, configurable architecture for easy customization

## Usage

Get those satisfying "plane overhead!" notifications:

```bash
# Track your local area (like HAL Airport, BLR - visible from my desk)
python3 aero_watch.py hal_area

# Watch the busy BLR Airport zone  
python3 aero_watch.py blr_airport

# Go big - monitor all of Bangalore
python3 aero_watch.py entire_blr
```

See what areas you can track:
```bash
python3 aero_watch.py --list-locations
```

## How It Works

The magic happens through publicly available ADS-B signals that aircraft broadcast. This data includes:
- Flight callsigns and routes
- Real-time position and altitude  
- Aircraft registration details

When a plane enters your defined area, you get a notification with:
- ✈️ Flight number and airline
- 📍 Route information (departure → arrival)
- 🔗 Clickable link to view live on ADSB Exchange

## Configuration

- `config/locations.json`: Define tracking areas with lat/lon boundaries
- `config/settings.json`: API settings, notification preferences, and tracking intervals

## Setup

First, get the dependencies:
```bash
pip3 install requests
```

For the satisfying macOS notifications (highly recommended):
```bash
brew install terminal-notifier
```

Then just run it and start plane-spotting from your desk! 🪟✈️

## Project Structure

```
aero-watch/
├── config/
│   ├── locations.json      # Geographic boundaries for tracking areas
│   └── settings.json       # API and notification settings
├── aero_watch.py          # Advanced tracker with notifications
├── flight_tracker.py      # Main tracking logic
├── flight_service.py      # OpenSky API integration
├── auth_manager.py        # OAuth2 authentication
├── notification_manager.py # macOS notification system
├── config_manager.py      # Configuration management
└── requirements.txt       # Python dependencies
```

## Built with ❤️ by

[Pankaj Tanwar](https://twitter.com/the2ndfloorguy), and checkout his [other side-hustles](https://pankajtanwar.in/side-hustles)