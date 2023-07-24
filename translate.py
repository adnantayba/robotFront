from googletrans import Translator
import time

def translateToEnglish(message):
    tr = Translator()
    out = tr.translate(message, dest="en")
    return out.text


def translateToArabic(message):
    tr = Translator()
    out = tr.translate(message, dest="ar")
    return out.text

start_time = time.time()
translateToEnglish('ارفع ايدك الشمال زاوية 90 درجة لمدة 5 ثواني')
end_time = time.time()
print(start_time - end_time)

def replace_word(sentence, word, word_replace):
    if word in sentence:
        return sentence.replace(word, word_replace)
    else:
        return sentence
    
