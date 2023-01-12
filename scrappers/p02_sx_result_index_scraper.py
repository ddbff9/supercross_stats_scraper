from bs4 import BeautifulSoup
from p00_general_functions import *


def getEventLinks():
    # Create/Initialize lists to store output and any errors:
    error_log = []
    output = []

    # Identify the web-page to scrape:
    url = "https://www.supercrosslive.com/ama-supercross-historical-results"

    # Call function to scrape the web-page
    page_html = scrapeHTML(url)

    # Find the tables that contain the links to each event:
    link_tables = page_html.find_all(class_="table-historical-class")

    # Loop over each table and parse event info:
    for table in link_tables:

        # Get list of link tags from table:
        event_link_tags = table.find_all('a')

        # Loop over each event:
        for event in event_link_tags:

            # Parse out link text:
            event_link = event.get('href')

            # Check if its the current event, if it is skip:
            if (event_link == '/current-event-results'):
                pass
            else:
                event_year = event_link[-4:]
                # Check if year is an int:
                try:
                    # If year is an int, store as such, otherwise add to error log:
                    event_year = int(event_year)
                except:
                    error_text = f'Error: {event_link} does not have a valid year!'
                    error_log.append(error_text)
                    pass

                # append root of url to link to make full link path:
                event_link = "https://www.supercrosslive.com" + event_link

                # append result to the output list
                output.append((event_year, event_link))

    return {'Links': output, 'Errors': error_log}
