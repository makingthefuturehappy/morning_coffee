import parser
import db

def scan(today):
    print("the Guardian")
    # today = today.replace("/", "-")
    url = "https://www.theguardian.com/world/americas"
    guardian = parser.Content(url, "the Guardian", today)

    # useful links selection
    for link in guardian.links_all:
        if today in link:
            # link = "https://www.reuters.com" + link
            guardian.links_useful.append(link)
        guardian.links_useful_qnnty = len(guardian.links_useful)

    guardian.get_news()
    print("The REUTERS scan is done\n")

    return guardian
