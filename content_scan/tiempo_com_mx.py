import parser

def scan(today, db):

  # the website is blocked
  print("La Tiempo MX")
  url = "http://tiempo.com.mx/"
  tiempo_mx = parser.Content(url, "La Tiempo MX", today)

  # useful links selection
  for link in tiempo_mx.links_all:
      try:
          if len(link) > 80:
              link = url[:-1] + link
              tiempo_mx.links_useful.append(link)
      except:
          pass

  tiempo_mx.links_useful = db.return_new_links(tiempo_mx.links_useful)
  db.save_new_links(tiempo_mx.links_useful)

  tiempo_mx.get_news()

    # set status for translation
  for news in tiempo_mx.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  tiempo_mx.links_useful_qnnty = len(tiempo_mx.links_useful)
  print("useful links qnnty:", tiempo_mx.links_useful_qnnty)
  print("La Tiempo MX scan is done\n")
  return tiempo_mx
