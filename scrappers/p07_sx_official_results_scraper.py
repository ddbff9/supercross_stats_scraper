from bs4 import BeautifulSoup
from ..private.sql_server import *
import pymysql
from p00_general_functions import *

# *********************************
# ****** SQL Server Settings ******
# *********************************

host_ = host_address
port_ = port_number
user_ = user_id
passwd_ = password
dbSchema = db_name

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
        str(eventSeason) + "%' AND sessionName = 'Official Results';"

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


def storeResults(list):

    # Connect to Sql database:
    sql_db = pymysql.connect(host=host_, port=port_,
                             user=user_, passwd=passwd_, db=dbSchema)

    # Define the table name to insert lap times into:
    dbTable = 'race_official_results'

    # Set cursor:
    cursor = sql_db.cursor()

    # list contains all combined qualifying results scraped from results page,
    # loop over combined qualifying results and insert the data into the SQL Database:
    for result in list:

        eventID = result[0]
        raceID = result[1]
        sessionID = result[2]
        sessionTitle = result[3]
        racePos = result[4]
        riderNum = result[5]
        riderName = result[6]
        riderBike = result[7]
        riderQual = result[8]
        riderHoleshot = result[9]
        riderLapsLed = result[10]
        riderPoints = result[11]

        # Attempt to insert data into SQL table:
        try:
            add_event = "INSERT INTO " + dbSchema + \
                "." + dbTable + \
                " (`eventID`, `raceID`, `sessionID`, `sessionTitle`, `racePos`, `riderNum`, `riderName`, `riderBike`, `riderQual`, `riderHoleshot`, `riderLapsLed`,`riderPoints`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

            # Data to send to SQL Table:
            data_event = (eventID, raceID, sessionID, sessionTitle, racePos, riderNum,
                          riderName, riderBike, riderQual, riderHoleshot, riderLapsLed, riderPoints)

            # Run the SQL Query:
            cursor.execute(add_event, data_event)

        # If error occurs while executing the SQL Insert Function,
        # report where issue occured:
        except:

            print("        Exception encountered: ", eventID, ', ', raceID, ', ', sessionID, ', ', sessionTitle, ', ', racePos,
                  ', #', riderNum, ', ', riderName, ', ', riderBike, ', ', riderQual, ', ', riderHoleshot, ', ', riderLapsLed, ', ', riderPoints)
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


def getOfficialResults(season):
    # Create a list of links to loop over. These links are to the URL
    # Index of results for that particular event.
    query_results = list(getResultsLinks(
        'eventID', 'raceID', 'sessionID', 'sessionHref', 'sx_results_session_links', season))

    # Create an empty list to store the links:
    session_hrefs = []

    # To save time inseting the data into SQL Database,
    # first scrape all results and store in a list,
    # then loop over that list inserting each list item into
    # the SQL database, followed by a single commit statement.
    season_official_results = []

    # query returns multiple columns, create a list of just the hrefs:
    for result in query_results:

        # Result[3] is column with href, extract that value and append to list:
        session_hrefs.append(result[3])

    # Get the HTML from each page in event_links:
    for t, session_href in enumerate(session_hrefs):

        # Href's are only half the url, concatenate https://www.supercrosslive.com to get full url:
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

        # Some sessions were labeled without a '-' in H3, so this will handle those exceptions:
        try:
            sessionTitle_parts = sessionTitle[0].text.split('-')
            sessionTitle = sessionTitle_parts[1].strip()
        except:
            sessionTitle

        # Get HTML for table that contains the results data:
        official_results_html = session_html.find_all(
            'table',  class_='responsive-table')

        # Find all tables on the results page:
        table = official_results_html[0]

        # The results are stored in multiple tables, one for each rider:
        official_table = table.find_all('tr')

        # Loop over each result table and extract the information:
        for result in official_table:

            # Get qualification position from table header row:
            officialPos_parts = result.find('th').text.split()

            # The first table on the page is empty and has an abbreviation
            # for Postion as Pos. and no number, thus the list created will
            # be 1 and should be skipped:
            if len(officialPos_parts) < 2:
                pass
            else:
                # Second position in list of Position parts contains the position number:
                officialPos = officialPos_parts[1].strip()

                # Table contents are in the same order for each table, thus grab text and
                # store to appropriate varaibles:
                riderNum = result.contents[2].text.strip()
                riderName = result.contents[4].text.strip()
                riderBike = result.contents[8].text.strip()
                riderQual = result.contents[10].text.strip()
                riderHoleshot = result.contents[12].text.strip()
                riderLapsLed = result.contents[14].text.strip()
                riderPoints = result.contents[18].text.strip()

                # Store the result info in a list:
                official_results_list = [eventID, raceID, sessionID, sessionTitle,
                                         officialPos, riderNum, riderName, riderBike, riderQual, riderHoleshot, riderLapsLed, riderPoints]

                # Append result data into the season_qual_results list:
                season_official_results.append(official_results_list)

    # Return the list that contains all the results for the season:
    return season_official_results

# *********************************
# ********* Main Function *********
# *********************************


print("\n    This program will scrape official results from Supercross racing")
print("    sessions stored on SupercrossLive.com and store this info in a")
print("    SQL Database.\n")

startYear = input("        Enter Year (2013 to Present): ")

print('\n        Program is scraping the official results...')

season_official_results_list = getOfficialResults(startYear)

print('\n        List Created, now adding official results to sql database, this will take a few minutes...\n')

storeResults(season_official_results_list)

print("\n        Completed! " + str(len(season_official_results_list)) +
      " results were stored in the SQL Database.\n")
