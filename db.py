def save_links(file_path, links:list):
  with open(file_path, "w") as file:
      for link in links:
          file.write(link + '\n')
  print("links are saved to", file_path)
  return

def read_links(file_path):
  links = []
  try:
    with open(file_path, "r") as file:
      for line in file:
        links.append(line[:-1])
  except:
    print("no file found", file_path)
  return links

def check_duplicate(links_exist:list, links_to_check:list):
  try:
    links = set(links_to_check) - set(links_exist)
  except:
    links = links_exist
  return list(links)