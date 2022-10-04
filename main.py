from channel import Channel
import logging

from joblib import dump, load
from datetime import datetime, date
from db import DB
import text_processor
import tg

def main():

    zero_shot_analysis = False
    tg_post = True
    emulate = True
    statistics = True

    today = str(date.today().strftime("%Y/%m/%d"))
    # today = "2022/09/09"
    db = DB("links.txt")

    # load channel settings
    channel_mexico = Channel('keys/mexico.yaml')
    channel_SA = Channel('keys/SA.yaml')
    channel_all_news = Channel('keys/all_news.yaml')
    channels = [
        # channel_mexico,
        # channel_SA,
        channel_all_news
    ]

    # load all key_words, refs, company_names etc
    geos = []
    companies = []
    refs = []

    for channel in channels:
        for geo in channel.geos:
            geos.append(geo)
        for company in channel.companies:
            geos.append(company)
        for ref in channel.companies:
            refs.append(ref)

    if emulate == False:
        from summarizer import Philschmid_bart_large_cnn_samsum
        # from zero_shot import bart_large_mnli
        import translate as translate

        # load NN models
        models = [
            # Pegasus(),
            # Facebook_bart_large_cnn(),
            Philschmid_bart_large_cnn_samsum(),
            # MT5_multilingual_XLSum(),
            # Small2bert_cnn_daily_mail(),
        ]

        # zero_shot = bart_large_mnli()

        # content parser
        import news_loader
        # news_sources = news_loader.news_loader(today, db)  # to keep news from all web sources
        news_sources = news_loader.auto_loader_v2(today, db)  # to keep news from all web sources

        # translate
        for source in news_sources:
            print(source.source_name)
            for news in source.news:
                if news['status'] == 'translate_from_esp':
                    news['title'] = translate.translate(news['title'])
                    traslated_text = translate.translate(news['text'])
                    # print("   -", news['title'])

                if news['status'] == 'translate_from_pt':
                    news['title'] = translate.translate(news['title'],
                                                        from_language='pt')

                    traslated_text = translate.translate(news['text'],
                                                        from_language='pt')


                if traslated_text != "translation error":
                    news['text'] = traslated_text
                    news['status'] = "to be sum"
                else:
                    news['status'] = 'translation error'

        # to process news
        print("\nSUMMARIZING")
        for source in news_sources:
            print(source.source_name)

            for news in source.news:

                # summarize
                if news['status'] == 'to be sum':
                    for model in models:
                        try:
                            print("   -", news['title'])
                            summary = model.summarize(news['text'])

                            #delete "dot" at the end for the correct sentence split of the last sentence
                            if '. ' in summary[len(summary)-2:]:
                              summary = summary[:-2]

                        except:
                            print(model.model_name)
                            logging.exception("some error happened\n")
                            news[model.model_name] = "fail"
                            news['status'] = 'model failed'
                            continue

                        summary = text_processor.clean_text(summary)
                        news['summary'] = summary
                        news['status'] = 'success'
                        news[model.model_name] = "success"

        # to_save
        dump(news_sources, 'news_sources.joblib')

    if emulate == True:
        news_sources = load('news_sources.joblib')

    # Tagging
    from tags import tags
    import news_ratings as rating

    for channel in channels:
        for source in news_sources:
            tags(source.news, channel)

            # display content
            for news in source.news:
                if news['status'] == 'success':
                    print("source:", source.source_name)
                    print(news['title'])
                    text_processor.pretty_print(news['summary'])
                    print("geo:", news['geo'])
                    print("companies:", news['companies'])
                    print("refs:", news['refs'])
                    print("url:", news['url'])

    # select the important
    print("\nTO SEND")
    to_send = []
    for source in news_sources:
        for news in source.news:
            if news['status'] == "success":
                to_send.append(news)

    # dispay the important
    for channel in channels:
        print("\nchannel:", channel.name)
        for news in to_send:
            print(news['title'])
            text_processor.pretty_print(news['summary'])
            print("geo:", news['geo'])
            print("companies:", news['companies'])
            print("refs:", news['refs'])
            print("rating:", news['rating'])
            print("url:", news['url'])

    # print statistics
    # print("summarization result:")
    # for source in news_sources:
    #     print("source:", source.source_name)
    #     print("links_all   :", len(source.links_all))
    #     print("useful      :", len(source.links_useful))
    #     for model in models:
    #         print("\n", model.model_name)
    #         fails = 0
    #         success = 0
    #         paywall = 0
    #         for news in source.news:
    #             if news["status"] == "fail":
    #                 fails += 1
    #             elif news["status"] == "success":
    #                 success += 1
    #             else:
    #                 news["status"] == "paywall"
    #                 paywall += 1
    #         print("success total:", success)
    #         print("paywall total:", paywall)
    #         print("sum failed total:", fails)


    # TG post
    if tg_post == True:

        for channel in channels:
            print("\nsent to channel:", channel.name)
            creds = {"chat_id": channel.chat_id,
                     "token": channel.token}
            for news in to_send:
                tg_post = tg.format_for_tg(
                    news['url'],
                    news['source'],
                    news['title'],
                    news['summary'],
                    news['tags'][channel.chat_id]
                )
                tg.send_msg(creds, tg_post)
                news['status'] = "sent"


    if statistics == True:
        import statistics
        statistics.summary(news_sources)

    return news_sources


start_time = datetime.now()
news_sources = main()
print("calc time:", datetime.now() - start_time)
