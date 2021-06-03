import re
import spacy
from spacy.tokenizer import Tokenizer
from src.stopwords import ENG_STOPWORDS, KEYWORDS

text = spacy.load("en_core_web_sm")
 
def extended_is_stop(token):
    
    text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)
    stop_words = text.Defaults.stop_words
    return token.is_stop or token.lower_ in stop_words or token.lemma_ in stop_words

def text_processor(docs):

    # Text normalization: remove numbers and special symbols, and split identifiers
    pattern = re.compile(r"[a-zA-Z][a-z]+|[A-Z]+")
    
    # Stopword Removal and lemmatization
    docs = [word.lemma_.lower() for word in text(str(pattern.findall(docs))) 
                            if not (extended_is_stop(word) or word.is_punct)]
                                    
    return docs