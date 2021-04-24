"""
Implement tokenizer and stemmer for bug reports and code,

and remove the stopwords and keywords
"""
from spacy.lang.en import English
from stopwords import ENG_STOPWORDS, KEYWORDS

text = English()
text.Defaults.stop_words.update(ENG_STOPWORDS, KEYWORDS)

def tokenizer(docs: list) -> dict:
    """multiprocessing tokenizer"""
    dict = {}
    for doc in text.pipe(docs, batch_size=300, n_process=8):
        
        
    return tokens

print(tokenizer(["I lobe k ","I jgeigje iyy"]))