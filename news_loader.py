# content parser
def news_loader(today,
                db,
                save_to_db=True,
                config_file="news_sources.yaml"):

    import parser
    import yaml
    import logging

    with open(config_file, 'r') as f:
        all_sources = list(yaml.safe_load(f))

    content = []

    for source in all_sources:
        try:
            url = source['URL']
            name = source['name']
            language = source['language']
            print(name)
            news_source = parser.Content(url,  # url
                                         name,  # source_name
                                         "",
                                         language=language)  # date
            for link in news_source.links_all:
                if link is not None:
                    if len(link) > 30:
                        if "https://" or "http://" in link:
                            if url in link:
                                news_source.links_useful.append(link)
                                print(link)
                        else:
                            real_link = url[:-1] + link
                            news_source.links_useful.append(real_link)
                            # print(real_link)
        except:
            logging.exception("can't get urls from", source)
            continue

        news_source.links_useful = db.return_new_links(news_source.links_useful)
        if save_to_db:
            db.save_new_links(news_source.links_useful)

        news_source.get_news()

        print("useful links:", len(news_source.links_useful))
        content.append(news_source)
    print("scan is done")
    return content