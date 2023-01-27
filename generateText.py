from googletrans import Translator
from wonderwords import RandomSentence

translator = Translator()
sentence = RandomSentence()
# 10, 'es'
def generateText(nSentences=10, language = 'en'):
    text = ""

    for i in range(nSentences):
        text += " " + sentence.sentence()
    try:
        translated_sentence = translator.translate(text, src='en', dest=language)
        translated_wanted_sentence = translated_sentence.text
        return [200, translated_wanted_sentence]
    except ValueError:
        print('Value error')
        return [500, 'Some values are incorrect (nPhrases is a Number and lan is a supported ISO language codes)']
    except:
        print('exception')
        return [500, 'Internal Server error']

    