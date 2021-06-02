import numpy as np
from gensim.corpora import Dictionary
from multiprocessing import Pool

def get_docu_feature(text_data):

    dct = Dictionary(text_data.values())

    dfs = np.zeros(len(dct), dtype=[("term", "a30"), ("df", "f4")])
    
    for i in range(len(dct)):
        dfs[i]["term"] = dct.__getitem__(i)
        dfs[i]["df"] = dct.dfs[i]
        
    idfs = np.zeros(len(dct), dtype=[("term", "a30"), ("idf", "f4")])
    idfs["term"] = dfs["term"]
    idfs["idf"] = np.log(len(text_data)/dfs["df"])

    return idfs

def get_term_feature(id_, cont, idfs):
    
    tf = np.zeros(idfs.size, dtype=[("id", "a250"), ("term", "a30"), ("tf", "f4"), ("lv_tf", "f4"), ("length", "f4"), ("norm", "f4")])
    
    tf["id"] = id_
    tf["term"] = idfs["term"]
    tf["length"] = len(cont)
    for term in cont:
        tf["tf"][tf["term"] == term.encode()] += 1
    tf["lv_tf"] = np.log(tf["tf"]) + 1
    tf["lv_tf"][np.isinf(tf["lv_tf"])] = 0
    
    return tf

def tfidf_creation(text_data, idfs):
    
    tfs = []

    pool = Pool(processes=8)
    for i, (id_, cont) in enumerate(text_data.items()):
        pool.apply_async(get_term_feature, args=(id_, cont, idfs), callback= tfs.append)
    pool.close()
    pool.join()

    tfs = np.array(tfs)
    tfs["norm"] = 1.0 / (1 + np.exp(- (tfs["length"] - np.min(tfs["length"])) / (np.max(tfs["length"]) - np.min(tfs["length"]))))

    tf_idfs = np.zeros(tfs.shape, dtype=[("id", "a250"),("term", "a30"), ("tf_idf", "f4"), ("norm", "f4")])
    idfs = np.tile(idfs, (tfs.shape[0], 1))
    tf_idfs["tf_idf"] = np.multiply(tfs["lv_tf"], idfs["idf"])
    tf_idfs["id"] = tfs["id"]
    tf_idfs["term"] = tfs["term"]
    tf_idfs["norm"] = tfs["norm"]
    
    return tf_idfs

