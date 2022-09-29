import translators as ts
import logging
import re

def translate(text,
              translator='google',
              from_language='es',
              to_language="en",
              attempts=3 # how many times split the text
              ):

    if translator == 'google':
        attempt = 0

        while attempt <= attempts:
            try:
                text = ts.google(text,
                                 from_language=from_language,
                                 to_language=to_language)
                return text
            except:
                attempt += 1
                # print("divide text into", attempt+1, "parts")
                traslated_text = ''
                parts = split_text(text, attempt+1)
                for part in parts:
                    try:
                        part = ts.google(part,
                                         from_language=from_language,
                                         to_language=to_language)
                        traslated_text += part
                        # print("    ", attempt+1, "parts: success\n")
                        return traslated_text
                    except:
                        attempt += 1
                        if attempt == attempts:
                            logging.exception("translation error!")
                        break

    else:
        print("translation modul error")
        text = "translation error"
        return text


def split_text(text, parts=2):

    i = len(text) // parts
    part_length = i
    all_parts = []
    text_start = 0
    text_end = len(text)

    for part in range(0, parts):
        # look for combination "senten[e. N]ew sentence"
        j = i + 4
        pattern = '([a-z])([.])(\s)([A-Z])'

        while j <= len(text):
            if re.search(pattern, text[i:j]) != None:  # end of the sentence search
                if part == parts:
                    text_end = len(text)
                else:
                    text_end = j-2
                all_parts.append(text[text_start:text_end])
                text_start = text_end+1
                i += part_length
                j = i + 4
                break
            else:
                i += 1
                j = i + 4
                continue
    all_parts.append(text[text_start:])
    return all_parts

