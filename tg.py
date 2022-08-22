import re

def clean_text(text):

  text = text.replace(" - ", "-")
  text = text.replace("u. s.", "US")
  text = text.replace("U.S.", "US")
  text = text.replace("u. n.", "UN")
  text = text.replace(" ’ ", "’")
  text = text.replace(" )", ")")
  text = text.replace("( ", "(")
  text = text.replace(" %", "%")
  text = text.replace("$ ", "$")

  pattern = '(\d[,])(\s)(\d)'
  repl = r'\1\3'
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

