import parser

def scan(today, db):

  # the website is blocked
  print("La Republica")
  url = "https://www.larepublica.co/"
  la_republica = parser.Content(url, "La Republica", today)

  # useful links selection
  for link in la_republica.links_all:
      try:
          if len(link) > 80:
              if "https://www.larepublica.co/" in link:
                  la_republica.links_useful.append(link)
      except:
          pass

  la_republica.links_useful = db.return_new_links(la_republica.links_useful)
  db.save_new_links(la_republica.links_useful)

  la_republica.get_news()

    # set status for translation
  for news in la_republica.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  la_republica.links_useful_qnnty = len(la_republica.links_useful)
  print("useful links qnnty:", la_republica.links_useful_qnnty)
  print("La Republica Empresas scan is done\n")
  return la_republica
