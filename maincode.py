import content_scan.latam as latam

news_sources = [] # to keep news from all web sources

cnbc = latam.cnbc()
economist = latam.economist()
news_sources.append(cnbc, economist)

print("all done")