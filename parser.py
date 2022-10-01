from bs4 import BeautifulSoup as bs
import requests
import logging

class Content():

  def __init__(self, url, source_name, date,
                min_text_size=500  # if the text is less than this size, it will be skipped
                ):
      self.url = url
      self.source_name = source_name
      self.date = date
      self.links_all = []
      self.links_useful = []  # links to be summarized
      self.links_failed = []  # links failed for summarization
      self.links_all_qnnty = None
      self.min_text_size = min_text_size
      self.links_skipped_qnnty = 0  # qnnty of links to be skipped

      # initial setup
      self.news = []  # list of dicts with news
      self.main_page = self.get_html(url, save_file=False)
      self.links_all = self.get_links(self.main_page)
      self.links_all_qnnty = len(self.links_all)
      print("total links (all types):", self.links_all_qnnty)

  def get_html(self, url,
                save_file=False  # if you want to save the html file
                ):
      header = {
          "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1"
          # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
      }
      try:
          html = requests.get(url, headers=header)
          if html.status_code == 200:
              html.encoding = "utf-8"
              if save_file:
                  with open("main_page.html", "w") as f:
                      f.write(html.text)
              return html
          else:
              print("can't get html from", self.url)
              print("status code:", html.status_code)
      except:
          logging.exception("can't get html page:", url)
          return None

  def get_links(self, html):
      content = bs(html.text, "html.parser")
      links = []
      all_links = content.find_all("a")
      for link in all_links:
          link = link.get("href")
          links.append(link)
      return set(links)

  def get_content(self, url):
      try:
          html = self.get_html(url)
          content = bs(html.text, "html.parser")
      except:
          print("can't html from:", url)
          title = ""
          text = ""
          return title, text

      try:
          title = content.find("h1").text
      except:
          try:
              title = content.find("h2").text
          except:
              title = "Can't get title by <h1> and <h2>"
              print(title, url)
              logging.exception("can't get html page:", url)

      content = content.find_all("p")
      text = ""
      for item in content:
          text += item.text
      return title, text

  def get_news(self):
      for link in self.links_useful:

          title, text = self.get_content(link)
          news = {"date": self.date,
                  "url": link,
                  "text": text,
                  "source": self.source_name,
                  "title": title,
                  "status": None,
                  "geo": [],
                  "companies": [],
                  "refs": [],
                  "rating": {} # "chat_id": "index priority"
                  }

          # paywall check
          if len(text) < self.min_text_size:
              self.links_skipped_qnnty += 1
              news['status'] = "paywall"
          else:
              news['status'] = "to be sum"

          self.news.append(news)

      return
