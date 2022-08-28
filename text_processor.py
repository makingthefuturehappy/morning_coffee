import re

def clean_text(text):

  text = text.replace(" - ", "-")
  text = text.replace("u. s.", "US")
  text = text.replace("U.S.", "US")
  text = text.replace("D.C.", "DC")
  text = text.replace("u. n.", "UN")
  text = text.replace("U.N.", "UN")
  text = text.replace(" ’ ", "’")
  text = text.replace(" )", ")")
  text = text.replace("( ", "(")
  text = text.replace(" %", "%")
  text = text.replace("$ ", "$")

  pattern = '(\d[,])(\s)(\d)'
  repl = r'\1\3'
  text = re.sub(pattern, repl, text)

  # St. Louis -> St.Louis
  pattern = r'(\s)([A-Z])([a-z])([.])(\s)([A-Z])'
  repl = r'\1\2\3\4\6'
  text = re.sub(pattern, repl, text)

  # Dec. 30 -> Dec,30
  pattern = r'([A-Z])([a-z])([a-z])(.)([0-9])([0-9])(\s)'
  repl = r'\1\2\3,\5\6\7'
  text = re.sub(pattern, repl, text)

  pattern = '(\d[.])(\s)(\d)'
  repl = r'\1\3'
  text = re.sub(pattern, repl, text)

  pattern = '(\w[.])(\s)(\d)'
  repl = r'\1\3'
  text = re.sub(pattern, repl, text)

  pattern = '([(])(\s)(\d)'
  repl = r'\1\3'
  text = re.sub(pattern, repl, text)

  pattern = '(\s)([)])'
  repl = r'\2'
  text = re.sub(pattern, repl, text)

  pattern = '(\s)([%])(\s)'
  repl = r'\2\3'
  text = re.sub(pattern, repl, text)

  return text

def pretty_print(text):
  text = text.split('. ')
  for sentence in text:
    sentence.replace(' - ', '-')
    print("-",sentence)
  print("\n")
  return

def clean_print_update(summary, news:dict):
  summary = clean_text(summary)
  pretty_print(summary)
  news.update({"summary": summary})
  print("\n")
  return
