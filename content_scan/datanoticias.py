import parser


def scan(today, db):
  print("DATANOTICIAS")
  url = "https://datanoticias.com/"
  datanoticias = parser.Content(url, "DATANOTICIAS", today)

  # useful links selection
  for link in datanoticias.links_all:
      if url in link:
          datanoticias.links_useful.append(link)
      datanoticias.links_useful_qnnty = len(datanoticias.links_useful)

  datanoticias.links_useful = db.return_new_links(datanoticias.links_useful)
  db.save_new_links(datanoticias.links_useful)

  datanoticias.get_news()


  # set status for translation
  for news in datanoticias.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  print("useful links qnnty:", datanoticias.links_useful_qnnty)
  print("The DATANOTICIAS scan is done\n")
  return datanoticias
