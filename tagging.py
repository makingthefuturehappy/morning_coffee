# categorizer

def tags(all_news, channel):
    for news in all_news:
        if news['status'] == "translated":

            for geo in channel.geos:
                # print("\n", news['source'])
                # print(news['status'])
                # print(news['text'])
                # print(channel.geos)
                if geo in news['text']:
                    news['geo'].append(geo)
            news['geo'] = list(set(news['geo']))

            for company in channel.companies:
                if company in news['text']:
                    news['companies'].append(company)
            news['companies'] = list(set(news['companies']))

            for ref in channel.refs:
                if ref in news['text']:
                    news['refs'].append(ref)
            news['refs'] = list(set(news['refs']))

            tags = news['geo'] + news['companies'] + news['refs']

            # add tags to the news
            try:
                news_tags = news['tags']
                news_tags.update({channel.chat_id: tags})
            except:
                news_tags = {channel.chat_id: tags}
            news.update({"tags": news_tags})

    return

def tags_v2(tags:list, news):
    all_tags = []

    if news['text'] == None:
        return news

    for tag in tags:
        if tag in news['text']:
            all_tags.append(tag)
    news['tags'] = set(all_tags)
    if len(news['tags']) != 0:
        news['status'] = "tagged"
    return news