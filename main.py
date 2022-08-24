from content_scan import latam as latam
from datetime import date
import text_processor
import tg
import yaml

def main(models):
    today = str(date.today().strftime("%Y/%m/%d"))

    # content parser
    news_sources = [] # to keep news from all web sources
    cnbc = latam.cnbc(today)
    # economist = latam.economist(today)
    news_sources.append(
        cnbc,
                        # economist
                        )
    print("news load is done\n")

    # summarize
    for source in news_sources:
        print("source:", source.source_name)

        for news in source.news:
            print(news['title'])
            news['text'] = text_processor.clean_text(news['text'])

            for model in models:
                print(model.model_name)
                # try:
                summary = model.summarize(news['text'])
                print("summary:\n", summary)
                # summary = text_processor.clean_print_update(summary)
                    # text_processor.clean_print_update(summary)

                    # update model statistics
                news.update({model.model_name: "success"})

                # except:
                #     print("some error happened\n")
                #     news.update({model.model_name: "fail"})
                #     continue

    # print statistics
    print("summarization result")
    for source in news_sources:
        print("source:", source.source_name)
        print("links_all   :", len(source.links_all))
        print("useful      :", len(source.links_useful))
        for model in models:
            print("\n", model.model_name)
            fails = 0
            success = 0
            for news in source.news:
                if news[model.model_name] == "fail":
                    fails += 1
                elif news[model.model_name] == "success":
                    success += 1
            print("success total:", success)
            print("failed total:", fails)

    # TG post

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    creds = {"chat_id": config['tg']['chat_id'],
             "token": config['tg']['token']}

    for source in news_sources:
        for news in source.news:
            try:
                tg_post = tg.format_for_tg(news['url'],
                                        source.source_name,
                                        news['title'],
                                        news['summary'],
                                        news['country'])
                # print(tg_post)
                # print("\n",tg_post)
                tg.send_msg(creds, tg_post)
            except:
                print("failed summarization:", news['title'])

    return
    # return news_sources