"""
use gensim to get cos similarity
"""
import math
from gensim.similarities import SparseMatrixSimilarity

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

def normalization(similarity: dict, code_length: dict):
    """
    use length function to normalization

    Args: dict, {path: code content}

    Returns: number
    """
    min_length = min(code_length.values())
    diff_length = max(code_length.values()) - min(code_length.values())
    alpha = 0.2
    norm_similarity = {}
    for bug_id, code_paths in similarity.items():
        for code_path in code_paths:
            code_path =(code_path[0], alpha * 1.0 / (1 + math.exp(code_length[code_path[0]] - min_length) / diff_length))

    return similarity


def compute_bugs_simi():
    """
    use gensim to get cos similarity between bugs

    Args: two dict, {path: bug information}, {ID: bug information}

    Returns: number
    """
    
    pass
