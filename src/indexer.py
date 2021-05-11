from gensim.models import TfidfModel
from gensim.corpora import Dictionary

# TODO: use gensim to compute idf and store tf matrices, see https://radimrehurek.com/gensim/corpora/mmcorpus.html

def index_creation(code_data: dict):
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
