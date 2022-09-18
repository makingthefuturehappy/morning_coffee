import parser

def scan(today, db):
  print("La Verdad Mexico")
  url = "https://laverdadnoticias.com/seccion/mexico/"
  la_verdad_mexico = parser.Content(url, "La Verdad Mexico", today)

  # useful links selection
  for link in la_verdad_mexico.links_all:
      try:
          if len(link) > 80:
              if "https://" in link:
                  la_verdad_mexico.links_useful.append(link)
              else:
                  link = url[:-1] + link
                  la_verdad_mexico.links_useful.append(link)
      except:
          pass

  la_verdad_mexico.links_useful = db.return_new_links(la_verdad_mexico.links_useful)
  db.save_new_links(la_verdad_mexico.links_useful)

  la_verdad_mexico.get_news()

    # set status for translation
  for news in la_verdad_mexico.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  la_verdad_mexico.links_useful_qnnty = len(la_verdad_mexico.links_useful)
  print("useful links qnnty:", la_verdad_mexico.links_useful_qnnty)
  print("La Verdad Mexico scan is done\n")
  return la_verdad_mexico
