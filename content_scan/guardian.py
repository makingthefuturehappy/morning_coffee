import parser
import db
from datetime import datetime
import re


def scan(today):
    print("the Guardian")
    date = datetime.strptime(today, '%Y/%m/%d')
    month = date.month
    months = {
        1: "jan",
        2: "aug",
        3: "mar",
        4: "apr",
        5: "may",
        6: "jun",
        7: "jul",
        8: "aug",
        9: "sep",
        10: 'oct',
        11: 'nov',
        12: 'dec'
    }

    month = str(months[month])
    year = str(date.year)
    day = str(date.day)
    today = str(year + '/' + month + '/' + day)

    url = "https://www.theguardian.com/world/americas"
    guardian = parser.Content(url, "the Guardian", today)

    # useful links selection

    for link in guardian.links_all:
        try:
            if today in link:
                guardian.links_useful.append(link)
        except:
            continue
    guardian.links_useful_qnnty = len(guardian.links_useful)

    guardian.get_news()

    print("useful links qnnty:", guardian.links_useful_qnnty)
    print("The REUTERS scan is done\n")

    return guardian
