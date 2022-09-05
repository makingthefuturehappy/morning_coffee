import parser

def scan(today):
  print("El Financiero")
  url = "https://www.elfinanciero.com.mx"
  financiero = parser.Content(url, "El Financiero", today)

  # useful links selection
  for link in financiero.links_all:
      if today in link:
          link = url + link
          financiero.links_useful.append(link)
      financiero.links_useful_qnnty = len(financiero.links_useful)

  financiero.get_news()
  for news in financiero.news:
      news['status'] = 'translate_from_esp'

  # paywall check by content text
  # for news in cnbc.news:
  #   if news['status'] != "paywall":
  #     if "Sign up for free newsletters" not in news['text']:
  #       continue
  #     else:
  #       news['status'] = 'paywall'
  #       print('paywall:', news['title'])
  print("El Financiero scan is done\n")
  return financiero
