# TODO: use gensim to compute idf
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

# TODO: use gensim to compute idf and store tf matrices, see https://radimrehurek.com/gensim/corpora/mmcorpus.html

def tf_computing(code_data: dict):
    """
    index the code files by their tf matrices,
    save .npy file

    Args: dict, {path: code content}

    Returns: dict, {path: index}
    """

    dct = Dictionary(dataset)
    corpus = [dct.doc2bow(line) for line in dataset]

    model = TfidfModel(corpus)
    vector = model[corpus[0]]

def idf_computing():
    """
    use gensim to compute idf, save tf-idf model

    Args: 

    Returns: 
    """
    pass
