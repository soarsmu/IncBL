"""
use gensim to get cos similarity
"""
import os
import math
from itertools import product
from more_itertools import map_reduce, flatten
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity

def compute_similarity(bug_data, code_data, dct, model):
    """
    use gensim to get cos similarity between bugs and codes

    Args: url, api keys

    Returns: dict
    """
    similarity = {}

    index = SparseMatrixSimilarity(model[code_data.values()], len(dct.token2id.keys()))

    for bug_id, bug_cont in bug_data.items():
        similarity[bug_id] = dict(zip(code_data.keys(), index[model[dct.doc2bow(bug_cont)]]))
    
    return similarity

def normalization(similarity: dict, code_length: dict):
    """
    use length function to normalization

    Args: dict, {path: code content}

    Returns: number
    """
    min_length = min(code_length.values())
    diff_length = max(code_length.values()) - min_length

    for bug_id, code_files in similarity.items():
        for code_path in code_files.keys():
            code_files[code_path] *= 1.0 / (1 + math.exp(-(code_length[code_path] - min_length) / diff_length))
        
    return similarity


def combine_bugs_simi(similarity:dict, fixed_files:dict, bug_data:dict, code_base_path:str):
    """
    use gensim to get cos similarity between bugs

    Args: two dict, {path: bug information}, {ID: bug information}

    Returns: number
    """
    alpha = 0.2
    dct = Dictionary(bug_data.values())

    for bug_id, bug_cont in bug_data.items():
        bug_data[bug_id] = dct.doc2bow(bug_cont)

    model = TfidfModel(corpus=bug_data.values(), smartirs="lfn")
    index = SparseMatrixSimilarity(model[bug_data.values()], len(dct.token2id.keys()))

    bug_simi = {}
    for bug_id, bug_cont in bug_data.items():
        bug_simi[bug_id] = dict(zip(bug_data.keys(), index[model[bug_cont]]))

    value_key_pairs = flatten(product(v,(k,)) for k,v in fixed_files.items())
    fixed_files = dict(map_reduce(value_key_pairs, lambda k:k[0], lambda k:k[1]))
    
    for bug_id, code_files in similarity.items():
        for code_path, simi_score in code_files.items():
            if code_path in fixed_files.keys():
                temp = 0
                for past_bug in fixed_files[code_path]:
                    temp += bug_simi[bug_id][past_bug]
                if bug_id in fixed_files[code_path] and len(fixed_files[code_path])>1:
                    temp = (temp - 1)/(len(fixed_files[code_path]) - 1)
                else:
                    temp /= len(fixed_files[code_path])
                
                code_files[code_path] = alpha*temp + (1-alpha)*simi_score

        similarity[bug_id] = dict(sorted(code_files.items(), key=lambda item: -item[1]))
        
    return similarity
