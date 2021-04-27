"""
Implement tokenizer and stemmer for bug reports and code,

and remove the stopwords and keywords
"""
from spacy.lang.en import English
from stopwords import ENG_STOPWORDS, KEYWORDS

text = English()
text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)

def tokenizer(docs: dict) -> dict:
    """multiprocessing tokenizer"""
    tokens = {}
    for doc in text.pipe(docs.values(), batch_size=300, n_process=8):
        print(doc.keys())
    return tokens

print(tokenizer({1:"I lobe k ", 2:"I jgeigje iyy"}))