"""
Implement tokenizer and lemmatization for bug reports and code,

and remove the stopwords, keywords and punctuation
"""
import re
import spacy
from spacy.tokenizer import Tokenizer
from src.stopwords import ENG_STOPWORDS, KEYWORDS

text = spacy.load("en_core_web_sm")
 
def extended_is_stop(token):
    """add new stopwords"""

    text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)
    stop_words = text.Defaults.stop_words
    return token.is_stop or token.lower_ in stop_words or token.lemma_ in stop_words

def text_processor(docs: dict) -> dict:
    """tokenizer, lemmatizer and remove stopwords"""

    tokens = {}

    # Text normalization: remove numbers and special symbols, and split identifiers
    pattern = re.compile(r"[a-zA-Z][a-z]+|[A-Z]+")
    for id_, conts in zip(docs.keys(), docs.values()):
        docs[id_] = str(pattern.findall(conts))
    
    # Stopword Removal and lemmatization
    for id_, conts in zip(docs.keys(), text.pipe(docs.values(), batch_size=300, n_process=8)):
        tokens.setdefault(id_, [cont.lemma_.lower() for cont in conts 
                                if not (extended_is_stop(cont) or cont.is_punct)])
    
    return tokens