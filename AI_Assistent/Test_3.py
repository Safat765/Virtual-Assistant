from googletrans import Translator

def translate_bengali_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, src='bn', dest='en')
    return translated_text.text

bengali_text = "আমি বাংলায় কথা বলতে পারি"
english_text = translate_bengali_to_english(bengali_text)
print("Translated Text:", english_text)
