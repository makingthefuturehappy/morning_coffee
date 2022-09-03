import parser

def scan(today, db):
  print("FOLHA")
  url = "https://www1.folha.uol.com.br/internacional/en/"
  folha = parser.Content(url, "FOLHA", today)
  today = today[:-2]

  # useful links selection
  for link in folha.links_all:
      try:
          if today in link:
            folha.links_useful.append(link)
      except:
          continue

  folha.links_useful = db.return_new_links(folha.links_useful)
  db.save_new_links(folha.links_useful)
  folha.links_useful_qnnty = len(folha.links_useful)

  folha.get_news()

  print("FOLHA scan is done\n")
  return folha