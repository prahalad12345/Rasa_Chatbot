


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import requests
import time
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

def distance(city1,city2):


    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"
    anotherurl='https://wft-geo-db.p.rapidapi.com/v1/geo/locations/'
    coninuation='/nearbyCities?radius=2&distanceUnit=MI&sort=-population&offset=0&limit=1'
    querystring = {"toCityId":"Q60"}
    city=city1
    anothherurl=url_api = "http://api.openweathermap.org/data/2.5/weather?appid=fd8d7aee7a3abd2babf88bff433775b8&q="
    responsse=requests.request("GET",anothherurl+city).json()
    headers = {
        "X-RapidAPI-Key": "f5e0cf1bebmsh7c5686020d6ecd4p1a8ac0jsnc5e3f224a34a",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    latitude=responsse['coord']['lon']
    longitude=responsse['coord']['lat']

    longitude=str(longitude)
    latitude=str(latitude)
    if latitude[0]!='-':
        latitude='+'+latitude

    coordinates=(longitude+latitude)

    response2 =  requests.request("GET", anotherurl+coordinates+coninuation, headers=headers).json()
    qid1=response2['data'][0]['wikiDataId']
    qid=response2['data'][0]['wikiDataId']+'/distance'

    time.sleep(1)

    city=city2
    response=requests.request("GET",anothherurl+city).json()

    latitude2=response['coord']['lon']
    longitude2=response['coord']['lat']

    longitude2=str(longitude2)
    latitude2=str(latitude2)
    if latitude2[0]!='-':
        latitude2='+'+latitude2

    coordinates2=(longitude2+latitude2)

    anotherurl='https://wft-geo-db.p.rapidapi.com/v1/geo/locations/'
    coninuation='/nearbyCities?radius=2&distanceUnit=MI&sort=-population&offset=0&limit=1'
    response22 =  requests.request("GET", anotherurl+coordinates2+coninuation, headers=headers).json()
    qid22=response22['data'][0]['wikiDataId']
    qid2=response22['data'][0]['wikiDataId']+'/distance'

    querystring["toCityId"]=qid22
    time.sleep(1)
    distance=requests.request("GET",'https://wft-geo-db.p.rapidapi.com/v1/geo/cities/'+qid1+'/distance',params=querystring,headers=headers).json()
    return distance


class ActionFindDistance(Action):

    def name(self) -> Text:
        return "find_distance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        city2 = tracker.get_slot('city2')
        print(city,' ',city2)
        if city is None:
            output = "Could not find the time zone for city1"
            dispatcher.utter_message(text=output)
            return []
        if city2 is None:
            output = "Could not find the time zone for city2"
            dispatcher.utter_message(text=output)
            return []
        distancee=distance(city,city2)

        if distance is None:
            output = "The distance doesn't exist"
        else:
            output = ('The distance for '+ city +' and '+city2+' is '+ str(distancee) +' miles')

        dispatcher.utter_message(text=output)

        return []
