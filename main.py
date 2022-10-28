import time

from channel import Channel
import logging

from joblib import dump, load
from datetime import datetime, date
from db import DB
import text_processor
import tg

def main():

    news_download_translate = True

    if news_download_translate == True:
        emulate = False
    else:
        emulate = True

    save_to_db = True
    to_sum = True #summarize
    tg_post = True
    statistics = False

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
    tags = []

    for channel in channels:
        for company in channel.companies:
            tags.append(company)
        for ref in channel.refs:
            tags.append(ref)

    # content parser
    if news_download_translate:
        import news_loader
        print("NEWS DOWNLOADING...")
        news_sources = news_loader.news_loader(today, db, save_to_db)  # to keep news from all web sources
        print("NEWS DOWNLOADING done")

        # translate
        print("\nNEWS TRANSLATING...")
        import translate as translate

        for source in news_sources:
            print(" -", source.source_name)
            for news in source.news:
                if news['status'] == "downloaded":
                    if news['title'] != None:
                        news['title'] = translate.translate(news['title'], from_language=news['language'])
                        print(news['title'])
                    traslated_text = translate.translate(news['text'], from_language=news['language'])
                    news['text'] = traslated_text

                    if traslated_text != "translation error":
                        news['status'] = "translated"
                    else:
                        news['status'] = 'translation error'
        print("\nTRANSLATING done")



    # select news by key words
    print("\nTAGGING...")
    news_to_sum = []

    import tagging

    for channel in channels:
        for source in news_sources:
            for news in source.news:
                news = tagging.tags_v2(tags, news)

                if news['status'] == "tagged":
                    print('\n', news['title'])
                    news_to_sum.append(news)

    # to sum news
    print("\nSUMMARIZING")

    if to_sum == True:
        from summarizer import Philschmid_bart_large_cnn_samsum
        # from zero_shot import bart_large_mnli

        # load NN models
        models = [
            # Pegasus(),
            # Facebook_bart_large_cnn(),
            Philschmid_bart_large_cnn_samsum(),
            # MT5_multilingual_XLSum(),
            # Small2bert_cnn_daily_mail(),
        ]

        for news in news_to_sum:
            print(news['source'])
            for model in models:
                try:
                    print(news['source'], ":", news['title'])
                    summary = model.summarize(news['text'])

                    # delete "dot" at the end for the correct sentence split of the last sentence
                    if '. ' in summary[len(summary) - 2:]:
                        summary = summary[:-2]

                except:
                    print(model.model_name)
                    logging.exception("some error happened\n")
                    news[model.model_name] = "fail"
                    news['status'] = 'model failed'
                    continue

                summary = text_processor.clean_text(summary)
                news['summary'] = summary
                news['status'] = 'summed'
                news[model.model_name] = "success"

        # to_save
        dump(news_sources, 'news_sources.joblib')
        print("NEWS DUMP done")

    if emulate == True:
        news_sources = load('news_sources.joblib')


    # dispay the important
    for news in news_to_sum:
        print(news['title'])
        text_processor.pretty_print(news['summary'])
        print("tags:", news['tags'])
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
            for news in news_to_sum:
                tg_post = tg.format_for_tg(
                    news['url'],
                    news['source'],
                    news['title'],
                    news['summary'],
                    news['tags']
                )

                time.sleep(2)
                tg.send_msg(creds, tg_post)
                news['status'] = "sent"


    if statistics == True:
        import statistics
        statistics.summary(news_sources)

    return news_sources


start_time = datetime.now()
news_sources = main()
print("calc time:", datetime.now() - start_time)
