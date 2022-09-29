# import parser
# import db
# from db import DB
#
# import logging
# from content_scan import forbes_mx as forbes_mx
#
# news_sources = []  # to keep news from all web sources
# db = DB("links.txt")
#
# # try:
# #     today = "2022/09/28"
# #     frbs_mx = forbes_mx.scan(today, db)
# #     news_sources.append(frbs_mx)
#
# # except:
# #     logging.exception("failed to load")
#
#
# urls = [
#     "https://www.forbes.com.mx/",
#     "https://www.cnbc.com/",
#     "https://www.buenosaires.gob.ar/",
#     # "https://www.clarin.com/tecnologia/",
#     "https://www.cnbc.com/",
#     "https://edition.cnn.com/americas",
#     "https://datanoticias.com/",
#     "https://www.economist.com/",
#     "https://www.elheraldo.co/",
#     "https://www.elfinanciero.com.mx",
#     "https://www1.folha.uol.com.br/internacional/en/",
#     "https://www.theguardian.com/world/americas",
#     "https://www.larepublica.co/",
#     "https://laopinion.com",
#     "https://www.latimes.com/topic/mexico-americas",
#     # "https://laverdadnoticias.com/seccion/mexico/",
#     "https://www.reuters.com/world/americas/",
#     "http://tiempo.com.mx/",
#     "https://vanguardia.com.mx/"
# ]
import parser

def auto_scan(urls:list, db):
    content = []
    for url in urls:
        print(url)
        news_source = parser.Content(url, url, "")
        for link in news_source.links_all:
            try:
                if link is not None:
                    if len(link) > 50:
                        if "https://" in link:
                                news_source.links_useful.append(link)
                        else:
                            news_source.links_useful.append(url[:-1] + link)
            except:
                logging.exception("link:", link)
                continue
        print("useful links:", len(news_source.links_useful))
        content.append(news_source)
    print("scan is done")
    return content
#
# today = "2022/09/28"
# content = scan_auto(urls, db)