"""
compute tf, df and idf matrices
"""
import numpy as np
from gensim.corpora import Dictionary

# TODO: use gensim to compute idf and store tf matrices, see https://radimrehurek.com/gensim/corpora/mmcorpus.html

def get_docu_feature(text_data):

    dct = Dictionary(text_data.values())

    dfs = np.zeros(len(dct), dtype=[("term", "a30"), ("df", "f4")])
    
    for i in range(len(dct)):
        dfs[i]["term"] = dct.__getitem__(i)
        dfs[i]["df"] = dct.dfs[i]
        
    idfs = np.zeros(len(dct), dtype=[("term", "a30"), ("df", "f4")])
    idfs["term"] = dfs["term"]
    idfs["df"] = np.log(len(text_data)/dfs["df"])

    return dfs, idfs

def get_term_feature(text_data, dfs):
    
    tfs = np.zeros((len(text_data), dfs.size), dtype=[("file", "a200"),("term", "a30"), ("tf", "f4")])
    tfs["term"] = dfs["term"]
    
    for i, (file_path, file_cont) in enumerate(text_data.items()):
        tfs[i]["file"] = file_path
        for term in file_cont:
            for j in range(tfs.shape[1]):
                if term.encode() == tfs[i][j]["term"]:
                    tfs[i][j]["tf"] += 1
                    continue
    
    lv_tfs = np.zeros(tfs.shape, dtype=[("file", "a250"),("term", "a30"), ("tf", "f4")])
    lv_tfs["tf"] = np.log(tfs["tf"]) + 1
    lv_tfs[np.isnan(lv_tfs["tf"])] = 0
    lv_tfs[np.isinf(lv_tfs["tf"])] = 0
    lv_tfs["term"] = tfs["term"]
    lv_tfs["file"] = tfs["file"]
    
    return lv_tfs

def tfidf_creation(tfs, idfs):
    
    tf_idfs = np.zeros(tfs.shape, dtype=[("file", "a250"),("term", "a30"), ("tf_idf", "f4")])
    idfs = np.tile(idfs, (tfs.shape[0], 1))
    print(idfs)
    tf_idfs = np.multiply(tfs, idfs)

    return tf_idfs

