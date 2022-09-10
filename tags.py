# categorizer

def tags(all_news, channel):
    for news in all_news:
        if news['status'] == "success":

            for geo in channel.geos:
                if geo in news['text']:
                    news['geo'].append(geo)

            for company in channel.companies:
                if company in news['text']:
                    news['companies'].append(company)

            for ref in channel.refs:
                if ref in news['text']:
                    news['refs'].append(ref)

    return