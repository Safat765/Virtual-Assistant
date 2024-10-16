from googletrans import Translator


def translate_to_bengali(text):
    translator = Translator()
    x = translator.translate(text, dest='bn').text

    return x


z = "Hello, how are you?"
translated_text = translate_to_bengali(z)
print(translated_text)
