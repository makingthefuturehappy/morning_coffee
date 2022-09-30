from channel import Channel
import logging

from summarizer import Philschmid_bart_large_cnn_samsum
# from zero_shot import bart_large_mnli
import translate as translate

from joblib import dump, load
from datetime import datetime, date
from db import DB
import text_processor
import tg


def main():

    start_time = datetime.now()

    zero_shot_analysis = False
    tg_post = True
    emulate = False

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
        news_sources = news_loader.auto_loader(today, db)  # to keep news from all web sources

        # translate
        print("translating from spanish to english...")
        for source in news_sources:
            print(source.source_name)
            for news in source.news:
                if news['status'] == 'translate_from_esp':
                    # print("title esp:", news['title'])
                    news['title'] = translate.translate(news['title'])
                    print("   -", news['title'])

                    traslated_text = translate.translate(news['text'])
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

            # news rating
            rating.mexico(source.news, channel)
            rating.SA(source.news, channel)
            rating.all_news(source.news, channel_all_news)

            # display content
            for news in source.news:
                if news['status'] == 'success':
                    print("\nchannel:", channel.name)
                    print("source:", source.source_name)
                    print(news['title'])
                    text_processor.pretty_print(news['summary'])
                    print("geo:", news['geo'])
                    print("companies:", news['companies'])
                    print("refs:", news['refs'])
                    print("rating:", news['rating'])
                    print("url:", news['url'])

    # select the important
    print("\nTO SEND")
    for channel in channels:
        to_send = []
        for source in news_sources:
            for news in source.news:
                if news['status'] == "success":
                    try:
                        if news['rating'][channel.chat_id] != 0:
                            to_send.append(news)
                    except:
                        continue


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



    # Zero-Shot labeling
    if zero_shot_analysis == True:
        print("ZERO-SHOT LABELING:")
        labels = channel_mexico.chat_id['zero_shots']

        for source in news_sources:
            for news in source.news:
                try:
                    print("\nsource:", source.source_name)
                    print(news['title'])
                    text_processor.pretty_print(news['summary'])
                    print(news['tags'])
                    news['zero_shot'] = zero_shot.zero_shot(news['text'], labels)
                    for shot in news['zero_shot']:
                        print(shot)
                    print("-----------------------------------\n")
                except:
                    continue

    # TG post
    if tg_post == True:

        for channel in channels:
            print("\nsent to channel:", channel.name)
            creds = {"chat_id": channel.chat_id,
                     "token": channel.token}
            for news in to_send:
                if channel.chat_id in list(news['rating'].keys()):
                    # try:
                    tg_post = tg.format_for_tg(
                        news['url'],
                        news['source'],
                        news['title'],
                        news['summary'],
                        news['tags'][channel.chat_id]
                    )
                    tg.send_msg(creds, tg_post)
                    # except:
                    #     print("failed to post news:", news['title'])

        return news_sources

    print("calc time:", datetime.now() - start_time)

news_sources = main()
