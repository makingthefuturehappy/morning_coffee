import parser
import db
import re

def scan(today):
  print("VANGUARDIA")
  # today = today.replace("/", "")
  url = "https://vanguardia.com.mx/"
  vangurdia = parser.Content(url, "VANGUARDIA", today)

  # useful links selection
  for link in vangurdia.links_all:
      try:
          if int(link[-5:]) > 0:
                # useful link has digits at the end
                # example: '/dinero/inauguran-7-congreso-internacional-de-excelencia-CI3820136'
              link = url[:-1] + link
              vangurdia.links_useful.append(link)
      except:
          continue
  vangurdia.links_useful_qnnty = len(vangurdia.links_useful)

  vangurdia.get_news()


  print("VANGUARDIA scan is done\n")
  return vangurdia
