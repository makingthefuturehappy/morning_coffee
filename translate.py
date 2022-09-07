import translators as ts

def translate(text, translator='google', from_language='es', to_language="en"):
    if translator == 'google':
        try:
            text = ts.google(text, from_language=from_language, to_language=to_language)
            return text
        except:
            print("translation error")
            text = "translation error"
            return text
    else:
        print("translation modul error")
        text = "translation error"
        return text