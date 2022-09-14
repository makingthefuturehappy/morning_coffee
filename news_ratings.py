# news rating for the channel

def mexico(all_news, channel):
    for news in all_news:
        if news['status'] == 'success':
            rating = 0
            if bool(news['companies']):
                rating += 100000 # show always in the channel

            if len(set(channel.geos) & set(news['geo'])) > 0:
                if len(set(channel.refs) & set(news['refs'])) > 0:
                    rating += len(news['refs'])

            if rating != 0:
                news['rating'].update({channel.chat_id: rating})
    return

def SA(all_news, channel):
    for news in all_news:
        if news['status'] == 'success':
            rating = 0
            if bool(news['companies']):
                rating += 100000 # show always in the channel

            if len(set(channel.geos) & set(news['geo'])) > 0:
                if len(set(channel.refs) & set(news['refs'])) > 0:
                    rating += len(news['refs'])

            if rating != 0:
                news['rating'].update({channel.chat_id: rating})
    return