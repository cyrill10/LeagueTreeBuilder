from requests_oauthlib import OAuth1
from xml.etree import ElementTree
import json
import time

import requests

auth = OAuth1('...', '...', '...', '...')

SIZE = [0, 1, 4, 16, 64, 256, 1_024, 1_024, 1_024, 1_024, 1024, 1_024]

countriesDict = {}

MAIN_PATH = "http://chpp.hattrick.org/chppxml.ashx?file=leaguedetails&version=1.5&leagueLevelUnitID={}"


maxLeagueCount = 0


LEAGUE_COUNT =258518

i = 1
loopCount = 0

while i <= LEAGUE_COUNT:
    answer = requests.get(MAIN_PATH.format(i), auth=auth)
    content = ElementTree.fromstring(answer.content)
    if (content.find("ErrorCode") != None or answer.status_code != 200):
        i+=1
        loopCount+=1
        continue
    
    seriesLevel = int(content.find("LeagueLevel").text)
    maxSeriesLevel = 11#int(content.find("MaxLevel").text)
    if (seriesLevel <= maxSeriesLevel) :   
        countryID = content.find("LeagueID").text
        
        
        if countryID in countriesDict:
            country = countriesDict[countryID]
        else:
            country = {};
            country['name'] = content.find("LeagueName").text
            
        
        
        if seriesLevel in country:
            seriesList = country[seriesLevel]
        else:
            seriesList =[];
        
        for j in range(i, i + SIZE[seriesLevel]):
            seriesList.append(j)
        country[seriesLevel] = seriesList
        countriesDict[countryID] = country
    
    i+=SIZE[seriesLevel]
    loopCount+=1
    print("i: ",i)
    print("---------")

    
    
print("Loop count: ", loopCount)

with open('countries.json', 'w') as json_file:
    json.dump(countriesDict, json_file)
    
    