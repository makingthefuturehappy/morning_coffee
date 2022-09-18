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


def news_loader(today, db):
    news_sources = []  # to keep news from all web sources

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