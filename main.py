from bs4 import BeautifulSoup
import requests

# Constants
# url to use
URL = 'https://shop.lululemon.com/p/womens-outerwear/Scuba-Oversized-12-Zip-Hoodie/_/prod9960807'
desiredColors = ['Lavender Dew', 'Pink Mist']


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


def main():
    flag = True
    while flag:
        colors = getColors()

        colors = wantedColors(colors)
        if len(colors) > 0:
            # Send message
            print(colors)
        flag = False


main()
