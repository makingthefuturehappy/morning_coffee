import content_scan.latam as latam
from datetime import date

def main():
    today = str(date.today().strftime("%Y/%m/%d"))
    news_sources = [] # to keep news from all web sources

    cnbc = latam.cnbc(today)
    # economist = latam.economist(today)
    news_sources.append(cnbc,
                        # economist
                        )
    print("all done")
    return news_sources