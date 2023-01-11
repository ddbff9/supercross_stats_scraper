from bs4 import BeautifulSoup
import requests

# *********************************
# ****** Scraping Functions *******
# *********************************


def scrapeHTML(site):

    # URL that scraper is looking up
    url = site

    # Set result to url that is requested:
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    return doc

# *********************************
# ******** Date Functions *********
# *********************************


def findMonth(month):

    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "Oct":
        return 10
    elif month == "November":
        return 11
    elif month == "December":
        return 12
    else:
        return "Error: Month is not listed in findMonth()!"


def convertDate(date):

    # NOTE: Date input is assumed to be like January 8, 2022
    #       and returns it in YYYY-MM-DD format.

    date_split = date.split(',')

    month_ = findMonth(date_split[0].split(' ')[0])
    day_ = date_split[0].split(' ')[1]
    year_ = date_split[1].strip()

    return str(year_) + "-" + str(month_) + "-" + str(day_)


def genPrimaryKey(date):

    # Date input is assumed to be like January 8, 2022
    #       and returns it in YYYYMMDD format.

    date_temp = date.split(',')
    month_ = findMonth(date_temp[0].split(' ')[0].title())
    day_ = date_temp[0].split(' ')[1]
    year_ = date_temp[1].strip()
    key = str(year_) + str(month_).zfill(2) + str(day_).zfill(2)

    return key

# *********************************
# ****** SX Points Function *******
# *********************************


def getRoundPos(points):

    if points == 0:
        return 'DNQ'
    elif points == 1:
        return 22
    elif points == 2:
        return 21
    elif points == 3:
        return 20
    elif points == 4:
        return 19
    elif points == 5:
        return 18
    elif points == 6:
        return 17
    elif points == 7:
        return 16
    elif points == 8:
        return 15
    elif points == 9:
        return 14
    elif points == 10:
        return 13
    elif points == 11:
        return 12
    elif points == 12:
        return 11
    elif points == 13:
        return 10
    elif points == 14:
        return 9
    elif points == 15:
        return 8
    elif points == 16:
        return 7
    elif points == 17:
        return 6
    elif points == 18:
        return 5
    elif points == 19:
        return 4
    elif points == 21:
        return 3
    elif points == 23:
        return 2
    elif points == 26:
        return 1
    else:
        return 'Error! Points Amount is not in Function!'
