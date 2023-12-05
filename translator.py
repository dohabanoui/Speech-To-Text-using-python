from googletrans import Translator

def translate_text(text, target_language):
    """
    translate a text to a given language
    params: 
        text: the text to translate
        target_language: the language to translate to
            values : ['en', 'ar', 'fr', 'es', 'it', 'de', 'pt', 'ru', 'ja', 'ko', 'zh-cn', 'tr']
    return: the translated text
    """

    # Creation d'une instance de la classe Translator
    translator = Translator()
    # traduction du texte
    translation = translator.translate(text, dest=target_language)
    return translation.text

# example
"""
text = "Hello, how are you?"
target_language = 'es'
translated_text = translate_text(text, target_language)
print(translated_text)
"""