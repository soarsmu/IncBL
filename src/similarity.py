import os
import math
import numpy as np
from itertools import product
from more_itertools import map_reduce, flatten
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity

def compute_similarity(bug_vector, code_vector, bug_ids, file_ids):
    
    similarity = np.zeros([bug_ids.size, file_ids.size])

    for bug_id in bug_ids:
        for file_id in file_ids:
            similarity[bug_ids == bug_id, file_ids == file_id] = 0.5 + 0.5 * np.sum(bug_vector[bug_ids == bug_id] * code_vector[file_ids == file_id])/(np.linalg.norm(bug_vector[bug_ids == bug_id]) *np.linalg.norm(code_vector[file_ids == file_id]))

    return similarity

def normalization(similarity, code_length, bug_ids, file_ids):
    
    min_length = min(code_length.values())
    diff_length = max(code_length.values()) - min_length

    for bug_id in bug_ids:
        for file_id in file_ids:
            similarity[bug_ids == bug_id, file_ids == file_id] *= 1.0 / (1 + math.exp(-(code_length[(file_id).decode()] - min_length) / diff_length))
        
    return similarity

def combine_bugs_simi(similarity, fixed_files, bug_data, bug_ids, file_ids):
    
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
    
    for bug_id in bug_ids:
        for file_id in file_ids:
            if file_id.decode() in fixed_files.keys():
                print(1)
                temp = 0
                for past_bug in fixed_files[file_id]:
                    temp += bug_simi[bug_id][past_bug]
                if bug_id in fixed_files[file_id] and len(fixed_files[file_id])>1:
                    temp = (temp - 1)/(len(fixed_files[file_id]) - 1)
                else:
                    temp /= len(fixed_files[file_id])

                similarity[bug_ids == bug_id, file_ids == file_id] =  (alpha*temp + (1-alpha)*similarity[bug_ids == bug_id, file_ids == file_id])
                # code_files[code_path] = alpha*temp + (1-alpha)*simi_score

        # similarity[bug_id] = dict(sorted(code_files.items(), key=lambda item: -item[1]))
        
    return similarity
