import parser
import db

def scan(today):
  print("CNBC")
  url = "https://www.cnbc.com/"
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
