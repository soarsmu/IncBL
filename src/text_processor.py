import re
import spacy
from spacy.tokenizer import Tokenizer
from src.stopwords import ENG_STOPWORDS, KEYWORDS

text = spacy.load("en_core_web_sm")
 
def extended_is_stop(token):
    
    text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)
    stop_words = text.Defaults.stop_words
    return token.is_stop or token.lower_ in stop_words or token.lemma_ in stop_words

def text_processor(docs: dict) -> dict:

    # Text normalization: remove numbers and special symbols, and split identifiers
    pattern = re.compile(r"[a-zA-Z][a-z]+|[A-Z]+")
    for id_, conts in docs.items():
        # Stopword Removal and lemmatization
        docs[id_] = [cont.lemma_.lower() for cont in text(str(pattern.findall(conts)))
                                if not (extended_is_stop(cont) or cont.is_punct)]
                                    
    return docs