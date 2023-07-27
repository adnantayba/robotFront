from langdetect import detect

def detect_language(text):
    try:
        language_code = detect(text)
        return language_code
    except:
        return None