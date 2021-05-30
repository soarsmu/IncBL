"""
compute tf, df and idf matrices
"""
import numpy as np
from gensim.corpora import Dictionary

# TODO: use gensim to compute idf and store tf matrices, see https://radimrehurek.com/gensim/corpora/mmcorpus.html

def get_docu_feature(text_data):

    dct = Dictionary(text_data.values())
    word_list = np.empty(len(dct), dtype = "a25")
    for i in range(len(dct)):
        word_list[i] = dct.__getitem__(i)
    
    dfs = np.zeros(word_list.size)
    for words in text_data.values():
        for word in words:
            dfs[word_list == (word).encode()] += 1

    idfs = np.log(len(text_data)/dfs)

    return word_list, dfs, idfs

def get_term_feature(word_list, text_data):
    
    file_id = np.empty(len(text_data), dtype = "a200")
    tfs = np.zeros([len(text_data), word_list.size])
    for i, (code_path, code_conts) in enumerate(text_data.items()):
        file_id[i] = code_path
        for code_cont in code_conts:
            tfs[i][word_list == (code_cont).encode()] += 1

    lv_tfs = np.log(tfs) + 1
    lv_tfs[np.isnan(lv_tfs)] = 0
    lv_tfs[np.isinf(lv_tfs)] = 0

    return file_id, lv_tfs

def tfidf_creation(file_id, tfs, idfs):
    
    idfs = np.tile(idfs, (file_id.size, 1))
    tf_idfs = np.multiply(tfs, idfs)

    return tf_idfs

