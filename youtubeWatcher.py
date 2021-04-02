#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import discord
import requests
import googleapiclient.discovery
from datetime import datetime
from time import sleep


#Turn on debug mode - doesn't send the discord notification
debug = False


############################################
#           SET THESE YOURSELF             #
############################################
youtube_api_key = ""
youtube_playlist_id = ""
webhook_url = ""


#Set this to a valid discord uid to enable user mentions in update messages, otherwise leave set to 0
discord_uid = 0
#How long do we sleep between checks
#30 seconds seemed reasonable, I don't recommend
#setting it much lower really. Change at your own
#risk!
sleep_period = 30


#Example provided directly in Google's API docs, just this bit of code is not by myself
def get_videos(api_key, playlist_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=5
    )
    response = request.execute()

    return(response)


#Helper function to save the dict of video titles as a means of persistency across runs
def saveTitles(titles, persist_file=".lastTitles"):
    try:
        with open(persist_file, "w") as f:
            for title in titles:
                f.write(title+'\n')
        return 1
    except Exception as e:
        print("Got an exception when trying to save persist file - {}".format(str(e)))
        return 0


#Basic variable initialisation 
foundNew = False
i = 0

#Feel free to modify this, I don't need more than a link to the video really...
ping_text="New LTT Video - https://youtube.com/watch?v={}"

#We load the last video titles that we know of. 
#Either we load them from a persistence file
#Or, if no such file exists, we initialise
#the list with empty values, guaranteeing
#the list will always exist with exactly 5
#elements
if os.path.isfile(".lastTitles"):
    with open(".lastTitles") as f:
        lastTitles = f.read().splitlines()
    if len(lastTitles) == 0:
        lastTitles = [None] * 5
else:
    lastTitles = [None] * 5

#If discord_uid set, add an explicit user mention.
#This way, when a new video comes out, the ping receiver
#Would have their Discord icon's mention tracker incremented
#+A big red 1 would show up by the source server's icon
if discord_uid != 0:
    ping_text="<@{}> ".format(discord_uid) + ping_text

#Main logic loop, fetch last 5 uploaded videos
#Check if we know of them all, and if not, send
#a ping for each new video to discord
while True:
    i = 0
    newTitles = list()
    foundNew = False
    now=datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #Just a little print to make sure the logic loop is working as intended
    print("[{}] Fetching uploads".format(now))

    videos = get_videos(youtube_api_key, youtube_playlist_id)
    #Here, we iterate over the latest 5 videos of a channel
    #If we find a new video, we let the user know and update
    #Our "known video titles"
    for item in videos['items']:
        if lastTitles[i] != item['snippet']['title']:
            foundNew = True
            print("New video found, sending ping - {}".format(item['snippet']['title']))
            if not debug:
                requests.post(webhook_url, json = {"content":ping_text.format(item['snippet']['resourceId']['videoId'])})
            newTitles.append(item['snippet']['title'])
        else:
            newTitles.append(item['snippet']['title'])
            i+=1
    if foundNew:
        lastTitles = newTitles
        if not saveTitles(lastTitles):
            print("Failed saving the titles, by this point it is safer to exit than to risk spamming your discord. Check system permissions?")
            exit(1)
    sleep(sleep_period)
