from bs4 import BeautifulSoup
from ..private.sql_server import *
import requests
import pymysql
from scrappers import p00_general_functions
from dataclasses import dataclass

"""
    This Program scrapes race event details from vault.racerxonline.com and stores them in a SQL Database.
"""

# *********************************
# ****** SQL Server Settings ******
# *********************************

host_ = host_address
port_ = port_number
user_ = user_id
passwd_ = password
db_ = db_name

# *********************************
# ********* SQL Functions *********
# *********************************


def storeEventInfo(startYear, endYear, type):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=db_)

    # Set cursor:
    cursor = sql_db.cursor()

    # Loop over each year:
    for i in range(int(startYear), (int(endYear) + 1)):

        # Call extractEventDetails function for the year in the loop and race type:
        season = extractEventDetails(i, type)

        # Loop over each event that occured during the year:
        for event in season:

            key = event['Key']
            type_ = event['Type']
            name = event['Event']
            venue = event['Venue']
            date = p00_general_functions.convertDate(event['Date'])
            city = event['City'].lstrip()
            state = event['State']

            try:
                add_event = "INSERT INTO " + db_ + \
                    ".`race_events` (`eventID`, `eventType`, `eventDate`, `eventName`, `eventVenue`,`eventCity`, `eventState`) VALUES (%s, %s, %s, %s, %s, %s, %s);"

                # Data to send to SQL Table:
                data_event = (key, type_, date, name, venue, city, state)

                # Run the SQL Query:
                cursor.execute(add_event, data_event)

            except:

                print("Exception encountered for race entry for",
                      event['Date'], "at", city)
                pass

        # Commit the season records to the database:
        sql_db.commit()

    # Disconnect from sql database:
    cursor.close()

    # Close sql database:
    sql_db.close()


def storeClassInfo(startYear, endYear, type):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=db_)

    # Set cursor:
    cursor = sql_db.cursor()

    # Loop over each year:
    for i in range(int(startYear), (int(endYear) + 1)):

        # Call extractEventDetails function for the year in the loop and race type:
        season = extractEventDetails(i, type)

        # Loop over each event that occured during the year:
        for event in season:

            key = event['Key']
            classes_ = event['Classes']

            for class_ in classes_:
                class_name = class_[0]
                class_hyper = class_[1]

                try:
                    add_event = "INSERT INTO " + db_ + \
                        ".`race_classes` (`eventID`, `eventClass`, `eventClass_Hyper`) VALUES (%s, %s, %s);"

                    # Data to send to SQL Table:
                    data_event = (key, class_name, class_hyper)

                    # Run the SQL Query:
                    cursor.execute(add_event, data_event)

                except:

                    print("Exception encountered for class entry for",
                          event['Date'], "at", event['City'])
                    pass

            # Commit the season records to the database:
            sql_db.commit()

    # Disconnect from sql database:
    cursor.close()

    # Close sql database:
    sql_db.close()


# *********************************
# ****** Scraping Functions *******
# *********************************

# Scrape Event Details in HTML from Racer X Vault:

def getEventsHtml(year, type):

    # URL that scraper is looking up
    url = 'https://vault.racerxonline.com/' + \
        str(year) + '/' + str(type) + '/races'

    # Set result to url that is requested:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    # Create a list of the html for each event on the page with a class of "clearfix":
    events_html = doc.find_all('li', class_='clearfix')

    return events_html


def extractEventDetails(year, type):

    # Create list to store races in:
    events = {}

    events_html = getEventsHtml(year, type)

    # Create list to store races in for the year:
    race_year = []

    # Loop over each events html to extract content
    for event_html in events_html:

        # Define the events name from event_html:
        event_name = event_html.contents[1].string

        # Find event details html from sub-list in event_html:
        html_event_details = event_html.contents[3]

        # Extract details from html:
        event_date = html_event_details.contents[0]

        # Generate the primary key for the event based off the date:
        event_PK = p00_general_functions.genPrimaryKey(event_date)

        # Split event location into list of venue, city, and state:
        event_location = html_event_details.contents[2].split(',')

        # Declare venue, city, and state from event_location list:
        if len(event_location) > 2:
            event_venue = event_location[0]
            event_city = event_location[1]
            event_state = event_location[2]
        else:
            event_venue = event_name
            event_city = event_location[0]
            event_state = event_location[1]

        # Extract Race Classes Details:
        race_classes_details = event_html.contents[5].find_all(class_='btn')

        # Create List to store individual events info in:
        race_class_details = []

        # Create List to store event race classes in:
        event_classes = []

        # Extract Race Classes Hyperlink:
        for race_class in race_classes_details:
            race_class_name = race_class.string
            race_class_hyper = race_class.get('href')
            race_class_details = (race_class_name, race_class_hyper)

            event_classes.append(race_class_details)

        race_year.append({'Key': event_PK, 'Type': type, 'Event': event_name, 'Venue': event_venue, 'Date': event_date,
                          'City': event_city, 'State': event_state, 'Classes': event_classes})

        events = race_year

    return events


# *********************************
# ********* Main Function *********
# *********************************

print("This program will find Motocross and Supercross")
print("race events in the RacerX Vault and store this")
print("info in a SQL Database.\n")

raceType = input("Enter a race type (SX or MX): ")
startYear = input("Enter Start Year: ")
endYear = input("Enter End Year: ")

print("\nAdding your events into database on your local server.\n")

# Add Event info to SQL Database in Events Table:
storeEventInfo(startYear, endYear, raceType)

# Add Class info for each event to SQL Database in Classes Table:
storeClassInfo(startYear, endYear, raceType)

print("\nCompleted! Your events should now be stored in the SQL Database.\n")
