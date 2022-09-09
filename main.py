from content_scan import economist as economist
from content_scan import reuters as reuters
from content_scan import guardian as guardian
from content_scan import cnn as cnn
from content_scan import vanguardia as vangurdia
from content_scan import folha as folha
from content_scan import cnbc as cnbc
from content_scan import latimes as latimes
from content_scan import financiero as financiero
from content_scan import laopinion as laopinion
from content_scan import elheraldo as elheraldo

from summarizer import Philschmid_bart_large_cnn_samsum
from zero_shot import bart_large_mnli

from joblib import dump, load
from datetime import date
from db import DB
import text_processor
import translate as translate
import tg
import yaml

def main():

    zero_shot_analysis = False
    tg_post = False

    today = str(date.today().strftime("%Y/%m/%d"))
    # today = "2022/09/09"
    db = DB("links.txt")

    # load key_words
    with open('keys/mexico.yaml', 'r') as f:
        mexico_keys = yaml.safe_load(f)
    geos = mexico_keys['geo']
    companies = mexico_keys['companies']
    refs = mexico_keys['refs']
    mexico_chat_id = mexico_keys['tg_keys']['chat_id']

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
    # fail
    # ELHERALDO = elheraldo.scan(today, db)
    # news_sources.append(ELHERALDO)

    # fail
    # ECONOMIST = economist.scan(today)
    # news_sources.append(ECONOMIST)

    CNBC = cnbc.scan(today)
    news_sources.append(CNBC)

    LAOPIMION = laopinion.scan(today)
    news_sources.append(LAOPIMION)

    CNN = cnn.scan(today)
    news_sources.append(CNN)

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

    FINANCIERO = financiero.scan(today)
    news_sources.append(FINANCIERO)

    print("news load is done\n")

    # translate
    print("translating from spanish to english...")
    for source in news_sources:
        # print("source:", source.source_name)
        for news in source.news:
            if news['status'] == 'translate_from_esp':
                # print("title esp:", news['title'])
                news['title'] = translate.translate(news['title'])
                # print("title eng:", news['title'], "\n")

                traslated_text = translate.translate(news['text'])
                if traslated_text != "translation error":
                    news['text'] = traslated_text
                    news['status'] = "to be sum"
                else:
                    news['status'] = 'translation error'

    # to process news
    for source in news_sources:
        print("source:", source.source_name)

        for news in source.news:

            # summarize
            if news['status'] == 'to be sum':
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

            # categorizer
            if news['status'] == "success":

                for geo in geos:
                    if geo in news['text']:
                        news['geo'].append(geo)
                news['geo'] = set(news['geo'])
                for company in companies:
                    if company in news['text']:
                        news['companies'].append(company)
                news['companies'] = set(news['companies'])
                for ref in refs:
                    if ref in news['text']:
                        news['refs'].append(ref)
                news['refs'] = set(news['refs'])

                # rating
                # mexico channel
                rating = 0
                rating += len(news['companies']) if bool(news['companies']) else 0

                if len(news['refs']) > 0 and len(news['geo']) > 0:
                    rating += len(news['refs'])
                    news['rating'].update({mexico_chat_id: rating})

                # display content
                print("\nsource:", source.source_name)
                print(news['title'])
                text_processor.pretty_print(news['summary'])
                print("geo:", news['geo'])
                print("companies:", news['companies'])
                print("refs:", news['refs'])
                print("rating:", news['rating'])
                print("url:", news['url'])


    # select the important
    print("\nTO SEND")
    to_send = []
    for source in news_sources:
        for news in source.news:
            if news['status'] == "success":
                try:
                    if news['rating'][mexico_chat_id] != 0:
                        to_send.append(news)
                except:
                    continue
    # dispay the important
    for news in to_send:
        print(news['title'])
        text_processor.pretty_print(news['summary'])
        print("geo:", news['geo'])
        print("companies:", news['companies'])
        print("refs:", news['refs'])
        print("rating:", news['rating'])
        print("url:", news['url'])



    # to_save
    dump(news_sources, 'news_sources.joblib')
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



    # Zero-Shot labeling
    if zero_shot_analysis == True:
        print("ZERO-SHOT LABELING:")
        labels = mexico_keys['zero_shots']

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
    if zero_shot_analysis == True:
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
