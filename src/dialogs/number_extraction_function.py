# function for extracting the number from a sentence
# we use this after detecting the degree value in the missing entity phase

from word2number import w2n
#from classes import language
#from classes import rra, language

singular = {
    "واحد": "1",
    "اثنان": "2",
    "ثلاثة": "3",   # Corrected the spelling here from "ثلاتة" to "ثلاثة"
    "اربع": "4",
    "خمس": "5",
    "ستة": "6",
    "سبعة": "7",
    "ثمانية": "8",
    "تسع": "9",
    "عشر": "10"
}

def extract_number_arabic(sentence, dictionary):
    words = sentence.split()  # Split the sentence into individual words
    for i, word in enumerate(words):
        if word in dictionary:
            words[i] = dictionary[word]  # Replace word with its numerical value if found in the dictionary
    converted_sentence = " ".join(words)  # Join the words back into a sentence
    return converted_sentence


def extract_number(text):
    try:
        
        text = extract_number_arabic(text, singular)
        # Split the text into individual words
        words = text.split()

        # Iterate over the words and convert them to numbers
        numbers = []
        for word in words:
            try:
                number = w2n.word_to_num(word)
                numbers.append(number)
            except ValueError:
                pass

        # Combine the numbers using custom logic
        if numbers:
            result = numbers[0]
            for i in range(1, len(numbers)):
                if numbers[i] < 100:
                    result += numbers[i]
                else:
                    result *= numbers[i]
            return result
        else:
            return None

    except ImportError:
        print("Please install the 'word2number' library to use this function.")

print(extract_number("90"))