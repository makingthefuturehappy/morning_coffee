# content parser
import logging

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
from content_scan import buenosaires as bsas
from content_scan import elheraldo as elheraldo
from content_scan import clarin_tech as clarin_tech
from content_scan import laverdad_mexico as laverdad_mexico
from content_scan import la_republica as la_republica
from content_scan import tiempo_com_mx as tiempo_com_mx
from content_scan import datanoticias as datanoticias
from content_scan import forbes_mx as forbes_mx
def news_loader(today, db):
    news_sources = []  # to keep news from all web sources

    try:
        frbs_mx = forbes_mx.scan(today, db)
        news_sources.append(frbs_mx)
    except:
        logging.exception("failed to load")

    try:
        dn = datanoticias.scan(today, db)
        news_sources.append(dn)
    except:
        logging.exception("failed to load")

    try:
        tiempo = tiempo_com_mx.scan(today, db)
        news_sources.append(tiempo)
    except:
        logging.exception("failed to load")

    try:
        republica = la_republica.scan(today, db)
        news_sources.append(republica)
    except:
        logging.exception("failed to load")

    try:
        verdad_mexico = laverdad_mexico.scan(today, db)
        news_sources.append(verdad_mexico)
    except:
        logging.exception("failed to load")

    try:
        ELHERALDO = elheraldo.scan(today, db)
        news_sources.append(ELHERALDO)
    except:
        logging.exception("failed to load")

    try:
        ECONOMIST = economist.scan(today)
        news_sources.append(ECONOMIST)
    except:
        logging.exception("failed to load")

    try:
        CLARIN_TECH = clarin_tech.scan(today, db)
        news_sources.append(CLARIN_TECH)
    except:
        logging.exception("failed to load")

    try:
        BSAS = bsas.scan(today, db)
        news_sources.append(BSAS)
    except:
        logging.exception("failed to load")

    try:
        CNBC = cnbc.scan(today)
        news_sources.append(CNBC)
    except:
        logging.exception("failed to load")

    try:
        LAOPIMION = laopinion.scan(today)
        news_sources.append(LAOPIMION)
    except:
        logging.exception("failed to load")

    try:
        CNN = cnn.scan(today)
        news_sources.append(CNN)
    except:
        logging.exception("failed to load")

    try:
        FOLHA = folha.scan(today, db)
        news_sources.append(FOLHA)
    except:
        logging.exception("failed to load")

    try:
        GUARDIAN = guardian.scan(today)
        news_sources.append(GUARDIAN)
    except:
        logging.exception("failed to load")

    try:
        LATIMES = latimes.scan(today)
        news_sources.append(LATIMES)
    except:
        logging.exception("failed to load")

    try:
        REUTERS = reuters.scan(today)
        news_sources.append(REUTERS)
    except:
        logging.exception("failed to load")

    try:
        VANGUARDIA = vangurdia.scan(today,db)
        news_sources.append(VANGUARDIA)
    except:
        logging.exception("failed to load")

    try:
        FINANCIERO = financiero.scan(today)
        news_sources.append(FINANCIERO)
    except:
        logging.exception("failed to load")

    print("news load is done\n")

    return news_sources

# auto loader
def auto_loader(today, db):
    import parser
    urls = [
        "https://www.forbes.com.mx/",
        "https://www.cnbc.com/",
        "https://www.buenosaires.gob.ar/",
        # "https://www.clarin.com/tecnologia/",
        "https://edition.cnn.com/americas",
        "https://datanoticias.com/",
        "https://www.economist.com/",
        "https://www.elheraldo.co/",
        "https://www.elfinanciero.com.mx",
        "https://www1.folha.uol.com.br/internacional/en/",
        "https://www.theguardian.com/world/americas",
        "https://www.larepublica.co/",
        "https://laopinion.com",
        "https://www.latimes.com/topic/mexico-americas",
        # "https://laverdadnoticias.com/seccion/mexico/",
        "https://www.reuters.com/world/americas/",
        "http://tiempo.com.mx/",
        "https://vanguardia.com.mx/"
    ]

    content = []
    for url in urls:
        print(url)
        news_source = parser.Content(url, # url
                                     url, # source_name
                                     "")  # date
        for link in news_source.links_all:
            if link is not None:
                if len(link) > 30:
                    if "https://" or "http://" in link:
                        if url in link:
                            news_source.links_useful.append(link)
                            print(link)
                    else:
                        real_link = url[:-1] + link
                        news_source.links_useful.append(real_link)
                        print(real_link)

        news_source.links_useful = db.return_new_links(news_source.links_useful)
        db.save_new_links(news_source.links_useful)
        
        news_source.get_news()

        # set status for translation
        for news in news_source.news:
            if news['status'] != 'paywall':
                news['status'] = 'translate_from_esp'

        print("useful links:", len(news_source.links_useful))
        content.append(news_source)
    print("scan is done")
    return content


def auto_loader_v2(today, db):
    import parser
    import yaml
    import logging

    news_sources = "news_sources.yaml"

    with open(news_sources, 'r') as f:
        all_sources = list(yaml.safe_load(f))

    content = []

    for source in all_sources:
        try:
            url = source['URL']
            name = source['name']
            language = source['language']
            print(name)
            news_source = parser.Content(url,  # url
                                         name,  # source_name
                                         "")  # date
            for link in news_source.links_all:
                if link is not None:
                    if len(link) > 30:
                        if "https://" or "http://" in link:
                            if url in link:
                                news_source.links_useful.append(link)
                                print(link)
                        else:
                            real_link = url[:-1] + link
                            news_source.links_useful.append(real_link)
                            print(real_link)
        except:
            logging.exception("can't get urls from", source)
            continue

        news_source.links_useful = db.return_new_links(news_source.links_useful)
        db.save_new_links(news_source.links_useful)

        news_source.get_news()

        # set status for translation
        for news in news_source.news:
            if news['status'] != 'paywall' and language == "esp":
                news['status'] = 'translate_from_esp'

        print("useful links:", len(news_source.links_useful))
        content.append(news_source)
    print("scan is done")
    return content