import re
import requests

def translate(text, src='en', dest='ru'):
  from googletrans import Translator

  translator = Translator()
  result = translator.translate('hello', src='en', dest='ru')

  translator = Translator()
  text = str(translator.translate(text, src=src, dest=dest).text) + "\n"
  return text


def format_for_tg(url, source_name, title, text, hashtags=[]):
  url = url.replace("https://", "")
  formatted_text = "\n" + "<b>" + "<a href =" + "'" + url + "'" + ">" + source_name + ":</a> " + title + "</b>" + "\n\n"

  text = text.split('. ')

  for sentence in text:
    sentence = "- " + sentence + "\n\n"
    formatted_text += sentence

  hasgtag_line = " "
  for hashtag in hashtags:
    hashtag = "%23" + hashtag + " "  # %23 is a hashtag symbol
    hasgtag_line += hashtag

  formatted_text += hasgtag_line
  return formatted_text

def send_msg(creds,  # chat, bot credentials
             text):
  url_req = "https://api.telegram.org/bot" + creds['token'] + \
            "/sendMessage" + "?chat_id=" + creds['chat_id'] + \
            "&text=" + text + \
            "&parse_mode=HTML" + \
            "&disable_web_page_preview=True"
  results = requests.get(url_req)
  return