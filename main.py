from bs4 import BeautifulSoup
import requests
from discord import Webhook, RequestsWebhookAdapter
import time

# Constants
DISCORD_URL = 'https://discord.com/api/webhooks/841543191428726845/hOKjaElgMf9cu1En2-2KbBWYYHaIteuzWSypVfXol9ofHwUywXQXLuVJ7epZXkA5lZgx'
URL = 'https://shop.lululemon.com/p/womens-outerwear/Scuba-Oversized-12-Zip-Hoodie/_/prod9960807'
desiredColors = ['Lavender Dew', 'Spiced Chai', 'desert sun', 'Black'] # Black is used for daily update that still working


# Returns list of current colors on lulu's website
def getColors():
    colors = []
    page = requests.get(URL).text
    soup = BeautifulSoup(page, features="lxml")
    images = soup.findAll('img')
    for i in images:
        colors.append(i.get('title'))
    return colors


# Searches for wanted colors on page
# O(m*n) m = desiredColors length, n = colors length
def wantedColors(colors):
    colorsFound = []
    for i in colors:
        for j in desiredColors:
            if str(i).lower() == str(j).lower():
                colorsFound.append(i)
    return colorsFound


# Sends message to discord webhook to display in server
def sendDiscordMsg(colors):
    msg = "Colors: " + str(colors) + " have become available"
    webhook = Webhook.from_url(DISCORD_URL, adapter=RequestsWebhookAdapter())
    webhook.send(msg)


# Every minute check if wanted color is available
# If found send message and remove color from checker for 12 hours
def main():
    foundColors = []
    flag = 0
    while True:
        colors = getColors()
        # 1440 minutes (1 day) has gone by
        # Re-add found colors and reset timer
        if flag == 1440:
            for color in foundColors:
                desiredColors.append(color)
                foundColors.remove(color)
                flag = 0

        colors = wantedColors(colors)
        # If wanted colors are found send message to discord
        if len(colors) > 0:
            # Send message
            sendDiscordMsg(colors)
            flag = 0
            # Do not relook for color if it was found for a few hours
            for color in colors:
                foundColors.append(color)
                desiredColors.remove(color)
        time.sleep(1*60)
        print(flag)
        flag += 1


main()
