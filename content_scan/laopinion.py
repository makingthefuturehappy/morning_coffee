import parser

def scan(today):
  print("la opinion")
  url = "https://laopinion.com"
  laopinion = parser.Content(url, "la opinion", today)

  # useful links selection
  for link in laopinion.links_all:
      if link is not None:
          if today in link:
              laopinion.links_useful.append(link)
          laopinion.links_useful_qnnty = len(laopinion.links_useful)

  laopinion.get_news()

    # set status for translation
  for news in laopinion.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  print("useful links qnnty:", laopinion.links_useful_qnnty)
  print("la opinion scan is done\n")
  return laopinion
