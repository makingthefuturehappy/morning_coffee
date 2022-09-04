import traslate
from content_scan import economist as economist
from content_scan import reuters as reuters
from content_scan import guardian as guardian
from content_scan import cnn as cnn
from content_scan import vanguardia as vangurdia
from content_scan import folha as folha
from content_scan import cnbc as cnbc
from content_scan import latimes as latimes

from summarizer import Philschmid_bart_large_cnn_samsum
from zero_shot import bart_large_mnli

from joblib import dump, load
from datetime import date
from db import DB
import text_processor
import traslate as translate
import tg
import yaml

def main():
    # today = str(date.today().strftime("%Y/%m/%d"))
    today = "2022/09/01"
    db = DB("links.txt")

    models = [
        # Pegasus(),
        # Facebook_bart_large_cnn(),
        Philschmid_bart_large_cnn_samsum(),
        # MT5_multilingual_XLSum(),
        # Small2bert_cnn_daily_mail(),
    ]

    zero_shot = bart_large_mnli()

    # content parser
    news_sources = []  # to keep news from all web sources
    # #
    CNBC = cnbc.scan(today)
    news_sources.append(CNBC)

    CNN = cnn.scan(today)
    news_sources.append(CNN)

    ECONOMIST = economist.scan(today)
    news_sources.append(ECONOMIST)

    FOLHA = folha.scan(today, db)
    news_sources.append(FOLHA)

    GUARDIAN = guardian.scan(today)
    news_sources.append(GUARDIAN)

    LATIMES = latimes.scan(today)
    news_sources.append(LATIMES)

    REUTERS = reuters.scan(today)
    news_sources.append(REUTERS)


    VANGUARDIA = vangurdia.scan(today,db)
    news_sources.append(VANGUARDIA)

    print("news load is done\n")

    # translate
    print("translating from spanish to english...")
    for source in news_sources:
        print("source:", source.source_name)
        for news in source.news:
            if news['status'] == 'translate_from_esp':
                print("title esp:", news['title'])
                news['title'] = traslate.translate(news['title'])
                print("title eng:", news['title'], "\n")
                news['text'] = traslate.translate(news['text'])

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
                    # text_processor.pretty_print(summary)

    # to_save
    # dump(news_sources, 'news_sources.joblib')
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

    # labeling
    print("ZERO-SHOT LABELING:")
    labels = ['politics', 'crime', 'taxi', 'natural disasters', 'mass murder', 'national holiday', 'flood']
    for source in news_sources:
        print("source:", source.source_name)
        for news in source.news:
            try:
                z_result = zero_shot.zero_shot(news['text'], labels)

                print(news['title'])
                text_processor.pretty_print(news['summary'])

                scores = z_result['scores']
                labels = z_result['labels']

                zero_shot_list = [] # to keep all zero-shot labels
                for i in range(0, len(labels)):
                    score = round(scores[i], 2)
                    zero_shot_list.append(str(labels[i]) + ": " + str(score))
                    news['zero_shot'] = zero_shot_list
                    print(labels[i], score)
                print("-----------------------------------\n")
            except:
                continue

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
