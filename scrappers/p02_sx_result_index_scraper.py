from bs4 import BeautifulSoup
from scrappers import p00_general_functions


def getEventLinks():
    url = "https://www.supercrosslive.com/ama-supercross-historical-results"
    page_html = p00_general_functions.scrapeHTML(url)

    # Two tables hold all links to supercross results since 2013:
    link_tables = page_html.find_all(class_="table-historical-class")

    output = []

    # Loop over each table and parse event info:
    for table in link_tables:
        # Get list of link tags from table:
        table_rows = table.find_all("tr")
        for row in table_rows:
            cells = row.find_all("td")
            for cell in cells:
                results_link = ''
                link_text = ''
                round_num = ''
                round_location = ''
                year = ''
                year = cell.get('data-table-header')

                try:
                    results_link = cell.find('a').get('href').strip()
                    link_text = cell.find('a').text.replace(
                        u'\xa0', u' ').strip(' ')
                    round_location = link_text.split(
                        '-')[1].replace(u'\xa0', u' ').strip(' ')
                    round_num = link_text.split(
                        '-')[0].replace(u'\xa0', u' ').strip(' ')
                    if (results_link == "/current-event-results"):
                        pass
                    else:
                        if results_link == '/event-results/05-anaheim-iii':
                            year = '2013'
                        if results_link == '/event-results/12-toronto':
                            year = '2014'
                        if year == None:
                            year = results_link[-4:]

                        output.append(
                            [year, round_num, round_location, results_link])
                except:
                    pass

    return output
