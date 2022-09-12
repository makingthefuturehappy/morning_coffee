import parser
import db

def scan(today, db):
  print("Buenos Aires")
  url = "https://www.buenosaires.gob.ar/"
  bsas = parser.Content(url, "Buenos Aires", today)

  # useful links selection
  for link in bsas.links_all:
      try:
          if "/noticias/" in link and "rss" not in link:
              if "buenosaires.gob.ar" in link:
                  bsas.links_useful.append(link)
              else:
                  link = url[:-1] + link
                  bsas.links_useful.append(link)
      except:
          continue

  bsas.links_useful = db.return_new_links(bsas.links_useful)
  db.save_new_links(bsas.links_useful)

  bsas.get_news()

    # set status for translation
  for news in bsas.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  bsas.links_useful_qnnty = len(bsas.links_useful)
  print("useful links qnnty:", bsas.links_useful_qnnty)
  print("Buenos Aires scan is done\n")
  return bsas
