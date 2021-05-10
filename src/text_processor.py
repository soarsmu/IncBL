"""
Implement tokenizer and lemmatization for bug reports and code,

and remove the stopwords, keywords and punctuation
"""

import spacy
from src.stopwords import ENG_STOPWORDS, KEYWORDS

text = spacy.load('en_core_web_sm')
text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)
lemmatizer = text.get_pipe("lemmatizer")
print(1)
def tokenizer(docs: dict) -> dict:
    """multiprocessing tokenizer"""

    tokens = {}
    for id_, conts in zip(docs.keys(), text.pipe(docs.values(), batch_size=300, n_process=8)):
        tokens.setdefault(id_, [cont.lemma_ for cont in conts \
                                if not (cont.is_stop or cont.is_punct)])
    return tokens