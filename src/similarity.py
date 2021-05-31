import os
import math
import numpy as np
from itertools import product
from more_itertools import map_reduce, flatten
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from gensim.similarities import SparseMatrixSimilarity

def compute_similarity(bug_vector, code_vector):
    alpha = 0.2
    similarity = np.zeros((bug_vector.shape[0], code_vector.shape[0]), dtype=[("bug", "a30"),("file", "a250"), ("score", "f4")])
    
    for i in range(bug_vector.shape[0]):
        similarity[i]["bug"] = bug_vector[i]["id"][0]
        for j in range(code_vector.shape[0]):
            similarity[i][j]["file"] = code_vector[j]["id"][0]
            similarity[i][j]["score"] = (0.5 + 0.5 * np.sum(bug_vector[i]["tf_idf"] * code_vector[j]["tf_idf"])/(np.linalg.norm(bug_vector[i]["tf_idf"]) * np.linalg.norm(code_vector[j]["tf_idf"]))) * code_vector[i][j]["norm"]

    return similarity

def bugs_similarity(bug_vector, fixed_files, bug_data):
    
    alpha = 0.2
    dct = Dictionary(bug_data.values())

    for bug_id, bug_cont in bug_data.items():
        bug_data[bug_id] = dct.doc2bow(bug_cont)

    model = TfidfModel(corpus=bug_data.values(), smartirs="lfn")
    index = SparseMatrixSimilarity(model[bug_rdata.values()], len(dct.token2id.keys()))

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
                
    return similarity
