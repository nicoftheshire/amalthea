import re
import nltk
from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer

class DataCleaner:
    def __init__(self, to_lang='en', from_lang='auto'):
        self.to_lang = to_lang
        self.from_lang = from_lang
        self.model_mapping = {
            'de': 'Helsinki-NLP/opus-mt-de-en',  # German to English
        }
        self.model = None
        self.tokenizer = None


    def is_english(self, text):
        try:
            language = detect(text)
            return language == 'en'
        except:
            return False

    def load_model(self, lang):
        if lang in self.model_mapping:
            model_name = self.model_mapping[lang]
            self.tokenizer = MarianTokenizer.from_pretrained(model_name)
            self.model = MarianMTModel.from_pretrained(model_name)

    def translate_to_english(self, text, detected_lang):
        self.load_model(detected_lang)
        if self.model is None or self.tokenizer is None:
            return text  # Return the original text if no suitable model is found

        # Split the text into sentences
        sentences = nltk.sent_tokenize(text)
        translated_sentences = []

        for sentence in sentences:
            # Tokenize the sentence using the new approach
            model_inputs = self.tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)

            # Generate translation using the model
            gen = self.model.generate(input_ids=model_inputs["input_ids"], attention_mask=model_inputs["attention_mask"])

            # Decode the generated text
            translated_sentence = self.tokenizer.batch_decode(gen, skip_special_tokens=True)
            translated_sentences.append(translated_sentence[0])

        # Join the translated sentences back together
        return ' '.join(translated_sentences)

    def clean_text(self, text):
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^.\w\s!?]', '', text)
        text = re.sub(r'\d+', '', text)
        text = text.lower()
        return text

    def clean_and_translate(self, text):
        cleaned_text = self.clean_text(text)  # Clean the text first
        translated = False
        detected_lang = detect(cleaned_text)
        if not self.is_english(cleaned_text):
            translated_text = self.translate_to_english(cleaned_text, detected_lang)
            translated = True
        else:
            translated_text = cleaned_text
        return translated_text, translated
