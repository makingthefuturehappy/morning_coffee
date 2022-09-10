import parser
import db

def scan(today, db):
  print("El heraldo")
  url = "https://www.elheraldo.co/"
  elheraldo = parser.Content(url, "El heraldo", today)

  # useful links selection
  for link in elheraldo.links_all:
      try:
          if int(link[-5:]) > 0:
                # useful link has digits at the end
                # example: '/dinero/inauguran-7-congreso-internacional-de-excelencia-CI3820136'
              link = url[:-1] + link
              elheraldo.links_useful.append(link)
      except:
          continue

  # elheraldo.links_useful = db.return_new_links(elheraldo.links_useful)
  # db.save_new_links(elheraldo.links_useful)
  # elheraldo.links_useful_qnnty = len(elheraldo.links_useful)
  elheraldo.get_news()

    # set status for translation
  for news in elheraldo.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  print("useful links qnnty:", elheraldo.links_useful_qnnty)
  print("El heraldo scan is done\n")
  return elheraldo
