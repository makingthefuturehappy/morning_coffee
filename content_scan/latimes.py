import parser, db
path = "/Users/alexander/PycharmProjects/"

def scan(today):
    print("Los Angeles Times")

    # path to links database
    file_path = path + "news/links.txt"
    url = "https://www.latimes.com/topic/mexico-americas"
    latimes = parser.Content(url, "LATIMES", today)

    # useful links selection
    line_to_search = "/world-nation/story/" + today.replace("/", "-")
    for link in latimes.links_all:
        if line_to_search in link:
            latimes.links_useful.append(link)

    # check dublicates
    file = open(file_path, 'r')
    links = file.readlines()
    links_saved = [link.rstrip('\n') for link in links]
    latimes.links_useful = db.check_duplicate(links_saved, latimes.links_useful)

    # db.save_links(file_path,
    #               links_saved + latimes.links_useful)

    latimes.get_news()
    latimes.links_useful_qnnty = len(latimes.links_useful)
    print("useful links qnnty:", latimes.links_useful_qnnty)
    print("LATIMES scan is done\n")

    return latimes