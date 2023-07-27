from googletrans import Translator, LANGUAGES

def translateToEnglish(message):
    tr = Translator()
    out = tr.translate(message, dest="en")
    return out.text


def translateToArabic(message):
    tr = Translator()
    out = tr.translate(message, dest="ar")
    return out.text

def replace_word(sentence, word, word_replace):
    if word in sentence:
        return sentence.replace(word, word_replace)
    else:
        return sentence
    
