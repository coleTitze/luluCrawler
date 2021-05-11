from bs4 import BeautifulSoup
import requests
from discord import Webhook, RequestsWebhookAdapter
import time

# Constants
DISCORD_URL = 'https://discord.com/api/webhooks/841543191428726845/hOKjaElgMf9cu1En2-2KbBWYYHaIteuzWSypVfXol9ofHwUywXQXLuVJ7epZXkA5lZgx'
URL = 'https://shop.lululemon.com/p/womens-outerwear/Scuba-Oversized-12-Zip-Hoodie/_/prod9960807'
desiredColors = ['Lavender Dew', 'Spiced Chai']


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
            if i == j:
                colorsFound.append(i)
    return colorsFound


# Sends message to discord webhook to display in server
def sendDiscordMsg(colors):
    msg = "Colors: " + str(colors) + " have become available"
    webhook = Webhook.from_url(DISCORD_URL, adapter=RequestsWebhookAdapter())
    webhook.send(msg)


# Every 3 minutes check if wanted color is available
def main():
    flag = True
    while flag:
        colors = getColors()

        colors = wantedColors(colors)
        # If wanted colors are found send message to discord
        if len(colors) > 0:
            # Send message
            sendDiscordMsg(colors)
        time.sleep(3*60)


main()
