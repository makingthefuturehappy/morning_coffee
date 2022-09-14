from datetime import date

class DB():
  def __init__(self, file_path):
    self.file_path = file_path
    self.saved_links = self.read_links()

  def read_links(self):
    saved_links = []
    try:
      with open(self.file_path, "r") as file:
        for line in file:
          saved_links.append(line[:-1])
    except:
      print("no file found", self.file_path)
    return saved_links

  def return_new_links(self, links_to_check:list):
    # return not dublicates
    try:
      new_links = set(links_to_check) - set(self.saved_links)
      return list(new_links)
    except:
      new_links = []
      return new_links

  def save_new_links(self, new_links:list):
    if len(new_links) != 0:
      with open(self.file_path, "a") as file:

          time_stamp = str(date.today().strftime("%Y/%m/%d"))
          file.write(time_stamp + '\n')

          for link in new_links:
            file.write(link + '\n')
      print("links are saved to", self.file_path)
    return

  def refresh_db(self, new_links):
    # read file and check dublicates
    link_to_save = self.return_new_links(new_links)
    self.save_new_links(link_to_save)
    return




