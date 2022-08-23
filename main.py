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
    economist = latam.economist(today)
    news_sources.append(
        # cnbc,
                        economist
                        )
    print("news load is done\n")

    # summarize
    for source in news_sources:
        print("source:", source.source_name)

        for news in source.news:
            print(news['title'])

            for model in models:

                try:
                    summary = model.summarize(news['text'])
                    text_processor.clean_print_update(summary)

                    # update model statistics
                    news.update({model.model_name: "success"})

                except:
                    print("some error happened\n")
                    news.update({model.model_name: "fail"})
                    continue

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

    cnbc.news = [{'date': '2022/08/20',
                 'url': 'https://www.bbc.com//news/world-latin-america-62544570',
                 'text': 'By Tiffany WertheimerBBC NewsGovernment officials in Ecuador have blamed a deadly explosion in the port city of Guayaquil on organised crime.At least five people were killed and 26 more injured in the blast on Sunday.Ecuador\'s interior minister said it was a "declaration of war" by criminal gangs against the government.The Andean country, which is used as a cocaine smuggling route from neighbouring Peru and Colombia, has seen a sharp rise in murders and gang-related crime recently.A state of emergency has been declared in Guayaquil, Ecuador\'s most populous city and an important trade hub. It is the fourth emergency to be declared in Ecuador since October because of gang violence.Eight houses and two cars were destroyed in the early morning blast, according to the National Risk and Emergency Management Service. Pictures from the scene show the front of houses ripped off and cars smeared in blood with their windows blown in.At a news conference late on Sunday, officials said the attack was directed at two men who go under the aliases of Cucaracha and Junior and are linked to Los Tiguerones, one of the leading crime gangs in Ecuador."Organized crime mercenaries, who have long drugged the economy, now attack with explosives," Interior Minister Patricio Carrillo tweeted after the blast."It is a declaration of war on the state," he said.Guayaquil has seen shocking levels of violence, including decapitated bodies hanging from pedestrian bridges and deadly prison riots between rival gangs. Nearly 400 inmates have been killed in six separate riots since February 2021.Following the explosion, the city\'s mayor, Cynthia Viteri wrote an open letter to President Guillermo Lasso, who took office last year."Criminal gangs have become a government within a government in Ecuador," the letter begins."We have witnessed people hanging from bridges, murders on motorcycles, rapes at shopping centres and on school buses," she wrote. "What else do you want us to do to defend ourselves? A President is the protector of his people, but so far we have not seen a single safe step to combat crime."On Twitter, Mr Lasso said he would "not allow organized crime to try to run the country", however he has faced an uphill battle and criticism over the lack of any meaningful change.Guayaquil has been ranked the 50th most violent city in the world by Insight Crime. The investigative journalism website reports that Ecuador\'s homicide rate increased faster than any other country in Latin America or the Caribbean in 2021.This video can not be playedEcuadorean journalist Blanca Moncada was on the front line of the Covid-19 crisis in her home town of GuayaquilPolice lose control of Ecuador townEcuador declares emergency over gang crime\'More than batons needed to control Ecuador\'s jails\'Deadly fighting erupts again at Ecuador jailMore drone attacks against Russia in Crimea - reportsFinnish PM reveals she has taken drug testEx-Briton \'Isis Beatle\' sentenced to life in prisonPeace at a price in the Talibanâ\x80\x99s heartlandsWaiting 38 years for a soldier lost on an icy battlefieldHow much grain is being shipped from Ukraine?Remembering the painful journey from Pakistan to India. VideoRemembering the painful journey from Pakistan to IndiaThe TikTok comedy stars trying to make it on stageLeaping, lava and lights: Photos of the weekThe castle at the centre of the Nazi\'s obsession with ancient mythsDid Freya the 94-stone walrus have to die?Russia must leave nuclear power plant - UN chiefTurkey\'s massive subterranean cityThe language with no known originWhy overthinkers struggle with remote workÂ© 2022 BBC. The BBC is not responsible for the content of external sites. Read about our approach to external linking.',
                 'title': "Ecuador: Guayaquil blast 'declaration of war' by gangs - officials",
                 'summary': 'At least five people were killed and 26 injured in an explosion in the port city of Guayaquil on Sunday. Interior Minister Patricio Carrillo said it was a "declaration of war" by criminal gangs against the government. The Andean country has seen a sharp rise in murders and gang-related crime recently. It is the fourth emergency declared in Ecuador since October over gang violence.',
                 'Philschmid_bart_large_cnn_samsum': 'success',
                 'country': ['Peru', 'Colombia']}]

    news_sources = [cnbc]

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

