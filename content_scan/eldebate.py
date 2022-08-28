import parser
import db

def scan(today):
  print("EL DEBATE")
  today = today.replace("/", "")
  url = "https://www.eldebate.com/"
  eldebate = parser.Content(url, "EL DEBATE", today)

  # useful links selection
  for link in eldebate.links_all:
      try:
          if today in link:
              eldebate.links_useful.append(url[:-1] + link)
      except:
          continue
  eldebate.links_useful_qnnty = len(eldebate.links_useful)

  eldebate.get_news()


  print("The EL DEBATE scan is done\n")
  return eldebate
