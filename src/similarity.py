"""
use Faiss or gensim to get cos similarity
"""

from gensim.similarities import SparseMatrixSimilarity

def compute_bugs_simi():
    """
    use Faiss or gensim to get cos similarity between bugs

    Args: two dict, {path: bug information}, {ID: bug information}

    Returns: number
    """
    pass


# TODO: use length function
def normalization():
    """
    use length function to normalization

    Args: dict, {path: code content}

    Returns: number
    """
    pass


def compute_similarity(bug_data, code_data, dct, model):
    """
    use gensim to get cos similarity between bugs and codes

    Args: url, api keys

    Returns: number
    """
    similarity = {}

    index = SparseMatrixSimilarity(model[code_data.values()], len(dct.token2id.keys()))

    for bug_id, bug_cont in bug_data.items():
        similarity[bug_id] = sorted(zip(code_data.keys(), index[model[dct.doc2bow(bug_cont)]]), key=lambda item: -item[1]) 

    return similarity

