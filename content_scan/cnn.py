import parser
import db

def scan(today):

  #parsing is blocked by CNN

  print("CNN")
  url = "https://edition.cnn.com/americas"
  cnn = parser.Content(url, "CNN", today)

  # useful links selection
  for link in cnn.links_all:
      try:
          if today in link:
              cnn.links_useful.append(link)
      except:
            continue
      cnn.links_useful_qnnty = len(cnn.links_useful)

  cnn.get_news()

  print("The CNN scan is done\n")
  return cnn
