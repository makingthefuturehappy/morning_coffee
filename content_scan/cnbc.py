import parser

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

  # paywall check by content text
  # for news in cnbc.news:
  #   if news['status'] != "paywall":
  #     if "Sign up for free newsletters" not in news['text']:
  #       continue
  #     else:
  #       news['status'] = 'paywall'
  #       print('paywall:', news['title'])
  print("useful links qnnty:", cnbc.links_useful_qnnty)
  print("The CNBC scan is done\n")
  return cnbc
