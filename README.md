# YoutubeWatcher
A simple Python script I cooked up as a solution to unreliable YouTube Upload notifications, both, from Youtube's own "Upload Notification Bell" and a few 3rd party solutions.

## Generic Requirements
- Python 3
- Discord account an a server with an administration level permission
- Google Cloud Platform API Key with an enabled Youtube Data API V3

## Python Library Dependency Installation
pip3 install google-api-python-client discord.py

## Acquiring necessary API keys, IDs etc
  
### Google API key
1. Go to https://console.cloud.google.com/ and create a project (Creating small projects with not too many requests / users is free)
2. Once created, you should be redirected to the project's dashboard
3. There, you need to first enable the use of the specific Youtube API:
    * Go to Library
    * Search for Youtube
    * Click on the "YouTube Data API v3"
    * Click Enable
4. Second, return to the project's Dashboard and go to Credentials
5. In the upper part of the screen, click "CREATE CREDENTIALS" - API key
    * I recommend restricting the key to a specific IP address, so that even if the key leaked, it wouldn't be usable to anyone else
6. Done, you have your API Key

### Discord Webhook URL
1. Open up settings of the server where you'll want to get your upload notifications
2. Under "Integrations - Webhooks" click "New Webhook", fill in the webhook's name + channel where the webhook user will post into
3. Copy Webhook URL

### Target playlist ID (In this case the "All Uploads" playlist ID)
1. Go to a target channel
2. Click the Videos tab
3. Click the "PLAY ALL" button next to "Uploads"
4. The target ID will be the value of the "list" query parameter in the URL

### Discord UID for optional mention in the notification messages
1. In Discord, go to User Settings
2. Click the little three dots next to your Avatar / Name / Badges and click "Copy ID"
