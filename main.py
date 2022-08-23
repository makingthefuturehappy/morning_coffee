from content_scan import latam as latam
from datetime import date
import text_processor

def main(models):
    today = str(date.today().strftime("%Y/%m/%d"))
    news_sources = [] # to keep news from all web sources

    cnbc = latam.cnbc(today)
    # economist = latam.economist(today)
    news_sources.append(cnbc,
                        # economist
                        )
    print("news load is done")


    for source in news_sources:
        print("source:", source.source_name)

        for news in source.news:
            print(news['title'])

            for model in models:

                try:
                    summary = model.summarize(news['text'])
                    text_processor.clean_print_update(summary)

                    # update model statistics
                    news.update({model.model_name: "success"})

                except:
                    print("some error happened\n")
                    news.update({model.model_name: "fail"})
                    continue
                    
    return news_sources

