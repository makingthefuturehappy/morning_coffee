from content_scan import economist as economist
from content_scan import reuters as reuters
from content_scan import guardian as guardian
from content_scan import cnn as cnn
from content_scan import vanguardia as vangurdia
from content_scan import folha as folha
from content_scan import cnbc as cnbc
from content_scan import latimes as latimes

from joblib import dump, load
from datetime import date
import text_processor
import tg
import yaml

def main():
    today = str(date.today().strftime("%Y/%m/%d"))

    # models = [
    #     # Pegasus(),
    #     # Facebook_bart_large_cnn(),
    #     Philschmid_bart_large_cnn_samsum(),
    #     # MT5_multilingual_XLSum(),
    #     # Small2bert_cnn_daily_mail(),
    # ]


    # content parser
    news_sources = []  # to keep news from all web sources
    #
    # LATIMES = latimes.scan(today)
    # news_sources.append(LATIMES)
    #
    # CNBC = cnbc.scan(today)
    # news_sources.append(CNBC)
    #
    # ECONOMIST = economist.scan(today)
    # news_sources.append(ECONOMIST)
    #
    # REUTERS = reuters.scan(today)
    # news_sources.append(REUTERS)
    #
    # GUARDIAN = guardian.scan(today)
    # news_sources.append(GUARDIAN)

    # VANGUARDIA = vangurdia.scan(today)
    # news_sources.append(VANGUARDIA)

    FOLHA = folha.scan(today)
    news_sources.append(FOLHA)

    # CNN = cnn.scan(today)
    # news_sources.append(CNN)

    print("news load is done\n")

    # summarize
    print("SUMMARIZATION:")
    for source in news_sources:
        print("source:", source.source_name)

        for news in source.news:
            print(news['title'])
            if news['status'] != 'paywall':
                for model in models:
                    try:
                        summary = model.summarize(news['text'])
                    except:
                        print(model.model_name)
                        print("some error happened\n")
                        news[model.model_name] = "fail"
                        news['status'] = 'model failed'
                        continue

                    summary = text_processor.clean_text(summary)
                    news['summary'] = summary
                    news['status'] = 'success'
                    news[model.model_name] = "success"
                    text_processor.pretty_print(summary)

    # # to_save
    # # dump(news_sources, 'news_sources.joblib')
    # news_sources = load('news_sources.joblib')


    # print statistics
    print("summarization result:")
    for source in news_sources:
        print("source:", source.source_name)
        print("links_all   :", len(source.links_all))
        print("useful      :", len(source.links_useful))
        for model in models:
            print("\n", model.model_name)
            fails = 0
            success = 0
            paywall = 0
            for news in source.news:
                if news["status"] == "fail":
                    fails += 1
                elif news["status"] == "success":
                    success += 1
                else:
                    news["status"] == "paywall"
                    paywall += 1
            print("success total:", success)
            print("paywall total:", paywall)
            print("sum failed total:", fails)


    # categorizer
    with open('key_words.yaml', 'r') as f:
        key_words = yaml.safe_load(f)

    geos = key_words['geo']
    companies = key_words['companies']
    all_tags = geos + companies

    for source in news_sources:
        for news in source.news:
            tags = []  # tags to be saved
            news['tags'] = tags
            for tag in all_tags:
                if tag in news['text']:
                    tags.append(tag)
                    news['tags'] = tags

            # to check qnnty off mentions
            # from collections import Counter
            # all_words = Counter([''.join(filter(str.isalpha, x.lower())) for x in news['text'].split() if
            #                          ''.join(filter(str.isalpha, x.lower()))])
            # for word, times in all_words.items():
            #     if word in all_tags:
            #         if times > 1:
            #             tags.append(word)
            # print(tags)
            # news['tags'] = tags

    # TG post
    with open('creds.yaml', 'r') as f:
        config = yaml.safe_load(f)

    creds = {"chat_id": config['tg']['chat_id'],
             "token": config['tg']['token']}
    for source in news_sources:
        for news in source.news:
            if news["status"] == 'success':
                try:
                    tg_post = tg.format_for_tg(
                        news['url'],
                        source.source_name,
                        news['title'],
                        news['summary'],
                        news['tags']
                    )
                    tg.send_msg(creds, tg_post)
                except:
                    print("failed to post:", news['title'])

    return news_sources

news_sources = main()
