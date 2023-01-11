import requests
from p00_general_functions import *
import re
from dataclasses import dataclass, asdict


@dataclass
class pulpEvent:
    eventID: str
    pulpID: str
    seriesType: str
    roundFormat: str
    roundLowScore: int
    roundAvgScore: float
    roundHighScore: int
    roundResultsURL: str


def getPulpEventDetails(year):

    # Event details are pulled via an api query:
    url = 'https://api.pulpmxfantasy.com/results'

    # To access the api, the following headers are required:
    headers = {
        'authority': 'api.pulpmxfantasy.com',
        'authorization': '140db2dbddb37411bcfb5af73b9963bbb100af9833c7543b9d35',
        'value': 'application/json, text/javascript, */*; q=0.01',
        'accept': 'application/json, text/javascript, */*; q=0.01'}

    # Request api data:
    page = requests.get(url, headers=headers)

    # Access the data, which is stored in .json format:
    rounds_data = page.json()['data']

    # list to store event data in to pass to sql database:
    rounds_list = []

    # Loop over each round and extract the data:
    for round_data in rounds_data:

        # Get Date:
        roundDate = round_data['prettyDate']

        # Date in api has day stored as 1st, 2nd, 3rd...
        # so we have to remove the alpha characters:
        roundDate_parts = roundDate.split()

        # Clean up the day value:
        dateDay = re.split(r'\D+', roundDate_parts[1])

        # Store the month and year value to rebuild the date value:
        dateMonth = roundDate_parts[0]
        dateYear = roundDate_parts[2].strip()

        # Rebuild the date in a traditional January 1, 2022 format:
        dateFixed = dateMonth.strip() + ' ' + \
            dateDay[0].strip() + ', ' + dateYear

        # Get series type (mx or sx):
        seriesType = round_data['type']

        if str(year) == dateYear:

            # Get the primary key by passing the date in traditional format to custom function:
            if seriesType == 'sx':
                eventID = 'S' + genPrimaryKey(dateFixed)
            else:
                eventID = 'M' + genPrimaryKey(dateFixed)

            # Asssign values to various round variables:
            pulpID = round_data['id']
            roundFormat = round_data['format']
            roundLowScore = round_data['lowScore']
            roundAvgScore = round_data['avgScore']
            roundHighScore = round_data['highScore']
            roundResultsURL = 'https://api.pulpmxfantasy.com/results/' + pulpID

            # store round information in a list and then append that list to rounds_list:
            rounds_list.append(pulpEvent(eventID, pulpID, seriesType, roundFormat,
                               roundLowScore, roundAvgScore, roundHighScore, roundResultsURL))

        else:
            pass

    print(asdict(rounds_list))
    return asdict(rounds_list)