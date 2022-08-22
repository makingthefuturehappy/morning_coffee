from bs4 import BeautifulSoup as bs
import requests

class Content():

  def __init__(self, url, source_name, date,
                min_text_size=350  # if the text is less than this size, it will be skipped
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
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
      }
      html = requests.get(url, headers=header)
      if html.status_code == 200:
          if save_file:
              with open("main_page.html", "w") as f:
                  f.write(html.text)
          return html
      else:
          print("can't get html from", self.url)
          print("status code:", html.status_code)
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
      html = self.get_html(url)
      content = bs(html.text, "html.parser")
      try:
          title = content.find("h1").text
      except:
          title = "No Title"
      content = content.find_all("p")
      text = ""
      for item in content:
          text += item.text
      return title, text

  def get_news(self):
      for link in self.links_useful:
          title, text = self.get_content(link)

          # paywall check
          if len(text) < self.min_text_size:
              self.links_skipped_qnnty += 1
              continue
          else:
              news = {"date": self.date,
                      "url": link,
                      "text": text,
                      "title": title}
              self.news.append(news)
      return self.news
