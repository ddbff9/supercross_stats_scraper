from bs4 import BeautifulSoup
import requests
import pymysql
from p00_general_functions import *

# *********************************
# ****** SQL Server Settings ******
# *********************************

host_ = '50.87.249.222'
port_ = int(3306)
user_ = 'danbaxin_admin'
passwd_ = 'M0t0cr055!'
dbSchema = 'danbaxin_WPZL5'

# *********************************
# ****** SQL Query Functions ******
# *********************************


def getResultsLinks(dbColumn1, dbColumn2, dbColumn3, dbColumn4, dbTable, eventSeason):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=dbSchema)

    # Set cursor:
    cursor = sql_db.cursor()

    # Define SQL Syntax for query:
    query = "SELECT " + dbColumn1 + ',' + dbColumn2 + ',' + dbColumn3 + ',' + dbColumn4 + \
            " FROM " + dbSchema + "." + dbTable +\
            " WHERE eventID like '" + \
        str(eventSeason) + \
        "%' AND sessionName = 'Individual Lap Times';"

    # Execute Query
    cursor.execute(query)

    # Store all rows returned in a list:
    query_results = cursor.fetchall()

    # Disconnect from sql database:
    cursor.close()

    # Close sql database:
    sql_db.close()

    return query_results

# *********************************
# ***** SQL Insert Functions ******
# *********************************


def storeLapTimes(list):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=dbSchema)

    # Define the table name to insert lap times into:
    dbTable = 'race_lap_times'

    # Set cursor:
    cursor = sql_db.cursor()

    # list contains all laps scraped from results page,
    # loop over laps and insert the data into the SQL Database:
    for lap in list:

        eventID = lap[0]
        raceID = lap[1]
        sessionID = lap[2]
        sessionTitle = lap[3]
        riderName = lap[4]
        riderNum = lap[5]
        lapNum = lap[6]
        lapTime_mins = lap[7]
        lapTime_secs = lap[8]

        # Attempt to insert data into SQL table:
        try:
            add_event = "INSERT INTO " + dbSchema + \
                "." + dbTable + \
                " (`eventID`, `raceID`, `sessionID`, `sessionTitle`, `riderName`,  `riderNum`, `lapNum`, `lapTime_mins`, `lapTime_secs`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"

            # Data to send to SQL Table:
            data_event = (eventID, raceID, sessionID, sessionTitle,
                          riderName, riderNum, lapNum, lapTime_mins, lapTime_secs)

            # Run the SQL Query:
            cursor.execute(add_event, data_event)

        # If error occurs while executing the SQL Insert Function,
        # report where issue occured:
        except:

            print("Exception encountered: ", eventID, ', ', raceID, ', ', sessionID, ', ', sessionTitle,
                  ', ', riderName, ', #', riderNum, ', ', lapNum, ', ', lapTime_mins, ', ', lapTime_secs)
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


def getLapTimes(season):
    # Create a list of links to loop over. These links are to the URL
    # Index of results for that particular event.
    query_results = list(getResultsLinks(
        'eventID', 'raceID', 'sessionID', 'sessionHref', 'sx_results_session_links', season))

    # Create an empty list to store the links:
    session_hrefs = []

    # To save time inseting the data into SQL Database,
    # first scrape all lap time data and store in a list,
    # then loop over that list inserting each list item into
    # the SQL database, followed by a single commit statement.
    season_laps = []

    # query returned multiple columns, create a list of just the hrefs:
    for result in query_results:

        # Result[3] is column with href, extract that value and append to list:
        session_hrefs.append(result[3])

    # Get the HTML from each page in event_links:
    for t, session_href in enumerate(session_hrefs):

        # Href's are only half the url, concatenat https://www.supercrosslive.com to href:
        url = 'https://www.supercrosslive.com' + session_href

        # Scrape the HTML from the event results page:
        session_html = scrapeHTML(url)

        # Assign values for eventID, raceID, and sessionID based on
        eventID = query_results[t][0]
        raceID = query_results[t][1]
        sessionID = query_results[t][2]

        # Find the Session Title, which is kept in H3 Tag:
        sessionTitle = session_html.find_all(
            'h3', class_="second-header-class")

        # 2020 had some session without a '-' in H3, so this will handle those exceptions:
        try:
            sessionTitle_parts = sessionTitle[0].text.split('-')
            sessionTitle = sessionTitle_parts[1]
        except:
            sessionTitle

        # Get HTML that contains the rider lap time data:
        rider_laps_html = session_html.find_all(
            'table', class_='table-rid-class')

        # Loop over the lap html for each lap in rider_laps_html:
        for rider_laps in rider_laps_html:

            # rider_laps returns html for a table, that table contains
            # a header row with rider number, name, and bike manufacturer.

            # Find header row HTML:
            table_header = rider_laps.find_all('th', class_='th-rid-class')

            # Assign header row values to variables

            # Cleanup value by removing # and stripping whitespace.
            riderNum = table_header[0].text.split('#')[1].strip()

            # Split Rider Num and Name
            riderName_Parts = table_header[1].text.split('-')

            # Store Rider Name, [:-3] removes the bike manufacture abbrv
            riderName = riderName_Parts[1].strip()[:-3].strip()

            # Find HTML for the rows in the lapt time table:
            table_rows = rider_laps.find_all('td')

            # Table has two columns, create lists to store column items in:
            column1 = []
            column2 = []

            # Loop over row values and store value in appropriate column:
            for i, row in enumerate(table_rows, 1):

                # table_rows is a list of all values extracted from table,
                # items in odd indexes belong in column1, even indexes belong
                # in column2

                # Check if loop iteration is even:
                if i % 2 == 0:

                    # If index is event store in column2:
                    column2.append(row.text)

                else:
                    # Index is odd, store in column1
                    column1.append(row.text)

            # Loop over column1, which contains lap numbers and possibly min, max, avg lap values
            for j, lap in enumerate(column1):

                # If len is > 2, then it is the min, max, or avg lap value, which we don't want, thus pass:
                if len(lap) > 2:
                    # If len is > 2, then it is the min, max, or avg lap value, which we don't want, thus pass:
                    pass

                else:

                    # Store lap number to variable:
                    lapNum = lap

                    # Lap times were stored as mins, e.g. 1:00.00
                    lapTime_mins = column2[j]

                    # To convert lap times to seconds, split lapTime_mins at the :
                    lapTime_parts = column2[j].split(':')

                    if len(lapTime_parts) > 1:
                        # If there was a :, then minutes will be index 0 position.
                        # To get total seconds, multiply minutes by 60s/min and add the
                        # seconds store in index 1:
                        lapTime_secs = int(
                            lapTime_parts[0]) * 60 + float(lapTime_parts[1])

                    else:
                        # If there wasn't a :, then returned list will only have one value
                        # which will be the seconds in a decimal format:
                        lapTime_secs = float(lapTime_parts[0])

                    # Each lap, create a list to store lap info in:
                    lap_list = [eventID, raceID, sessionID, sessionTitle,
                                riderName, riderNum, lapNum, lapTime_mins, lapTime_secs]

                    # Append each lap into the season list that this function will then output:
                    season_laps.append(lap_list)

    return season_laps

# *********************************
# ********* Main Function *********
# *********************************


print("\nThis program will scrape laptime data from Supercross Qualifying and ")
print("racing sessions from race results stored on SupercrossLive.com")
print("and store this info in a SQL Database.\n")

startYear = input("Enter Year (2013 to Present): ")

print('\nProgram is scraping the lap times, this will take a few minutes...')

season_lap_list = getLapTimes(startYear)

print('List Created, now adding lap data to sql database, this will take approximately 30 minutes....')

storeLapTimes(season_lap_list)
print("\nCompleted! Your laps should now be stored in the SQL Database.\n")
