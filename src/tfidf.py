"""
compute tf, df and idf matrices
"""
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

# TODO: use gensim to compute idf and store tf matrices, see https://radimrehurek.com/gensim/corpora/mmcorpus.html

def tfidf_computing(code_data: dict):
    """
    index the code files by their tf matrices,
    save .npy file

    Args: dict, {path: code content}

    Returns: dict, {path: index}
    """
    
    dct = Dictionary(code_data.values())

    for code_path, code_cont in code_data.items():
        code_data[code_path] = dct.doc2bow(code_cont)

    model = TfidfModel(corpus=code_data.values(), smartirs="lfn")

    # TODO: save tf, idf
    
    return code_data, dct, model

