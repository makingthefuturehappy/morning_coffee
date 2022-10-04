

def summary(news_sources):
    total_all_news = 0

    all_success = 0
    all_translated = 0
    all_translation_error = 0
    all_summarization_error = 0

    for source in news_sources:
        total_news = len(source.news)
        total_all_news += total_news
        translated = 0
        translation_error = 0
        summarization_error = 0
        success = 0

        for news in source.news:
            if news['status'] == "to be sum":
                translated += 1
                all_translated += 1
            if news['status'] == "translation error":
                translation_error += 1
                all_translation_error += 1
            if news['status'] == 'success':
                success += 1
                all_success += 1
            if news['status'] == 'model failed':
                summarization_error += 1
                all_summarization_error += 1

        print("\nsource:            ", source.source_name)
        print("total news:          ", total_news)
        print(" success:            ", success)
        if translated != 0:
            print(" translated:         ", translated)
        if translation_error != 0:
            print(" translation error:  ", translation_error)
        if summarization_error != 0:
            print(" summarization error:  ", summarization_error)

    print("\ntotal_all_news:", total_all_news)
    print("all_success:", all_success)
    print("all_translated:", all_translated)
    print("all_translation_error:", all_translation_error)
    print("all_summarization_error:", all_summarization_error)