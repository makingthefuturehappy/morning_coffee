import parser

def scan(today, db):
  print("Clarin Tech")
  url = "https://www.clarin.com/tecnologia/"
  clarin_tech = parser.Content(url, "Clarin Tech", today)

  # useful links selection
  for link in clarin_tech.links_all:
      try:
          if len(link) > 80:
              if "https://" in link:
                  clarin_tech.links_useful.append(link)
              else:
                  link = url[:-1] + link
                  clarin_tech.links_useful.append(link)
      except:
          pass

  clarin_tech.links_useful = db.return_new_links(clarin_tech.links_useful)
  db.save_new_links(clarin_tech.links_useful)

  clarin_tech.get_news()

    # set status for translation
  for news in clarin_tech.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  clarin_tech.links_useful_qnnty = len(clarin_tech.links_useful)
  print("useful links qnnty:", clarin_tech.links_useful_qnnty)
  print("Clarin Tech scan is done\n")
  return clarin_tech
