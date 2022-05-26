import os
import telebot
import spacy
import wikipedia
from transformers import PegasusForConditionalGeneration, PegasusTokenizer


class SummaryArticle:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
        self.model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

    def messageHandler(self, text):
        doc = self.nlp(text)
        #take out punctuations, spaces and shows the base of the words
        clean_doc = [token.text for token in doc if not token.is_stop and not token.is_punct \
                     and not token.is_space]
        return ' '.join(clean_doc)

    def search(self, token):
        # search for a term
        result = wikipedia.search(token)
        # get the page: Neural network
        page = wikipedia.page(result[0])
        # get the whole wikipedia page text (content)
        content = page.content
        return content

    def summarize(self, token):
        # Create tokens - number representation of our text
        tokens = self.tokenizer(token, truncation=True, padding="longest", return_tensors="pt")
        # Summarize
        summary = self.model.generate(**tokens)
        # Decode summary
        return self.tokenizer.decode(summary[0])

    def process(self, message):
        text = self.messageHandler(message)
        search_results = self.search(text)
        summary = self.summarize(search_results)
        return summary
