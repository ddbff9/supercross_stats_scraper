from bs4 import BeautifulSoup
import requests
import pymysql
from p00_general_functions import *

'''
This program loops over all the Supercross Events listed on https://www.supercrosslive.com/ama-supercross-historical-results. It pulls in the link to each event from the SQL Database and then scrapes the links from that event page.

The objective is to create a SQL Table with the eventID, raceID, and eventHref for each session that riders lap times were recorded. It can also be used to get entry lists for the event as well as results.

'''
# *********************************
# ****** SQL Server Settings ******
# *********************************


host_ = '50.87.249.222'
port_ = int(3306)
user_ = 'danbaxin_admin'
passwd_ = 'M0t0cr055!'
dbSchema = 'danbaxin_WPZL5'

# *********************************
# ***** SQL Insert Functions ******
# *********************************


def storeEventInfo(eventID, raceID, sessionID, sessionName, sessionHref):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=dbSchema)

    dbTable = 'sx_results_session_links'

    # Set cursor:
    cursor = sql_db.cursor()

    try:
        add_event = "INSERT INTO " + dbSchema + \
            "." + dbTable + \
            " (`eventID`, `raceID`, `sessionID`, `sessionName`, `sessionHref`) VALUES (%s, %s, %s, %s, %s);"

        # Data to send to SQL Table:
        data_event = (eventID, raceID, sessionID, sessionName, sessionHref)

        # Run the SQL Query:
        cursor.execute(add_event, data_event)

    except:

        print("Exception encountered", eventID, '-', sessionName)
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


def getResultsLinks(sessionName):

    url = 'https://www.supercrosslive.com/current-event-results'

    # Get the HTML from the event results page:
    event_results_index = scrapeHTML(url)

    # Get date of the event:
    eventDate = event_results_index.find(id='eventdates').text

    # Generate the event ID from the Date:
    eventID = genPrimaryKey(eventDate)

    # Find all link tags
    linkTags = event_results_index.find_all('a', text=sessionName)

    if linkTags == []:
        pass
    else:

        for link in linkTags:
            sessionHref = link.get('href')
            sessionName = link.text.title()
            sessionHref_parts = sessionHref.split('/')

            if len(sessionHref_parts) <= 6:
                raceID = sessionHref_parts[4]
                sessionID = sessionHref_parts[5][:-5]
            else:
                raceID = sessionHref_parts[6]
                sessionID = sessionHref_parts[7][:-5]
                sessionHref = '/' + sessionHref_parts[3] + '/' + sessionHref_parts[4] + '/' + \
                    sessionHref_parts[5] + '/' + \
                    sessionHref_parts[6] + '/' + sessionHref_parts[7]

            # TODO: Store eventID, sessionClass, sessionTitle, sessionHref to database:
            storeEventInfo(eventID, raceID, sessionID,
                            sessionName, sessionHref)
            # !! Uncomment to see output while running
            # print('eventID:', eventID, '\nraceID:', raceID,
            #       '\nsessionID:', sessionID, '\nsessionHref:', sessionHref)
            # print()


# *********************************
# ********* Main Function *********
# *********************************


print("This program will scrape links to Supercross Qualifying and ")
print("racing results for Supercross races on SupercrossLive.com")
print("and store this info in a SQL Database.\n")

print("\nNext enter a session that you would like to get results for,")
print("here are some options:")
print('    • entry list')
print('    • Best Lap Times')
print('    • Combined Qualifying Times')
print('    • Fastest Segment Times')
print('    • Individual Lap Times')
print('    • Individual Segment Times')
print('    • Lap Chart')
print('    • Provisional Point Standings')
print('    • Provisional Results')
print('    • Standings')
print('    • Starting Lineup')
sessionDesc = input("\nEnter name of Session to get links for: ")

print("\nAdding your links into database on your local server.\n")

getResultsLinks(sessionDesc)

print("\nCompleted! Your events should now be stored in the SQL Database.\n")
