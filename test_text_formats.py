import text_processor
from joblib import dump, load
# #to_save
# dump(news_sources[0].news, 'list_of_dict.joblib')

#to_load
# #############################
news_sources = [] # to keep news from all sources
news_sources = load('news_sources.joblib')

all_news = news_sources[1].news
for news in all_news:
    if news['status'] == 'success':
        summary = news['summary']
        print(summary)
        summary = text_processor.clean_text(summary)
        print(summary)
        text_processor.pretty_print(summary)

print("done")