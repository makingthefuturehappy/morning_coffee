##############################
import parser
from datetime import date

def cnbc():
  print("CNBC")
  url = "https://www.cnbc.com/"
  today = str(date.today().strftime("%Y/%m/%d"))

  cnbc = parser.Content(url, "CNBC", today)

  # useful links selection
  for link in cnbc.links_all:
      if today in link:
          cnbc.links_useful.append(link)
      cnbc.links_useful_qnnty = len(cnbc.links_useful)

  cnbc.get_news()
  # paywall check
  all_news = []
  for news in cnbc.news:
    if "Sign up for free newsletters" not in news['text']:
      all_news.append(news)
      # cnbc.news.remove(news)
    else:
      print('was not able to parse')
      cnbc.links_skipped_qnnty += 1
  cnbc.news = all_news

  print("useful links qnnty:", cnbc.links_useful_qnnty)
  print("The CNBC scan is done\n")
  
  return cnbc

############################
def economist():
  print("The Economist")
  url = "https://www.economist.com/"
  today = str(date.today().strftime("%Y/%m/%d"))
  economist = parser.Content(url, "The Economist", today)

  # useful links selection
  for link in economist.links_all:
      if today in link:
          link = url + link
          economist.links_useful.append(link)
      economist.links_useful_qnnty = len(economist.links_useful)

  economist.get_news()
  print("useful links qnnty:", economist.links_useful_qnnty)
  print("The Economist scan is done\n")

  return economist