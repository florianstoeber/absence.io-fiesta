# Absence.io time tracker helper

## Install
- `git clone`
- run `pip --user install -r requirements.txt`
- change the following in `track.py` with your absence.io API credentials
 
````
USER_ID = '<user_id>'
API_KEY = '<api_key>'
TIMEZONE_NAME = 'CET'
TIMEZONE = '+0100'
````

## Run
- run `python3 track.py start` to start tracking
- run `python3 track.py pause-start` to start breaks
- run `python3 track.py stop` to stop tracking and breaks