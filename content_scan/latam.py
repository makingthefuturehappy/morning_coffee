##############################
import parser
import db



############################
def economist(today):
  print("The Economist")
  url = "https://www.economist.com/"
  economist = parser.Content(url, "The Economist", today)

  # useful links selection
  for link in economist.links_all:
      if today in link:
          link = url + link
          economist.links_useful.append(link)
      economist.links_useful_qnnty = len(economist.links_useful)

  economist.get_news()
  print("useful links qnnty:", economist.links_useful_qnnty)
  print("The Economist scan is done\n")

  return economist

##############################