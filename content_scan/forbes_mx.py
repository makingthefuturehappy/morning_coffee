import parser


def scan(today, db):
  print("Forbes MX")
  url = "https://www.forbes.com.mx/"
  forbes_mx = parser.Content(url, "FORBES MX", today)

  # useful links selection
  for link in forbes_mx.links_all:
      try:
          if len(link) > 80:
              if "https://www.forbes.com.mx/" in link:
                  forbes_mx.links_useful.append(link)
      except:
          pass

  forbes_mx.links_useful = db.return_new_links(forbes_mx.links_useful)
  db.save_new_links(forbes_mx.links_useful)

  forbes_mx.get_news()


  # set status for translation
  for news in forbes_mx.news:
      if news['status'] != 'paywall':
          news['status'] = 'translate_from_esp'

  forbes_mx.links_useful_qnnty = len(forbes_mx.links_useful)
  print("useful links qnnty:", forbes_mx.links_useful_qnnty)
  print("The FORBES MX scan is done\n")
  return forbes_mx
