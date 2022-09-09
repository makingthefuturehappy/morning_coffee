import parser
import db

def scan(today):
  print("REUTERS")
  today = today.replace("/", "-")
  url = "https://www.reuters.com/world/americas/"
  reuters = parser.Content(url, "REUTERS", today)

  # useful links selection
  for link in reuters.links_all:
      if today in link:
          link = "https://www.reuters.com" + link
          reuters.links_useful.append(link)
      reuters.links_useful_qnnty = len(reuters.links_useful)

  reuters.get_news()
  print("useful links qnnty:", reuters.links_useful_qnnty)
  print("The REUTERS scan is done\n")

  return reuters
