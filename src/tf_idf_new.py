import json
import os
import math
import numpy as np
from gensim.models.tfidfmodel import df2idf
from gensim.models import TfidfModel
from gensim.corpora import Dictionary, MmCorpus
from multiprocessing import Pool, Process, Queue, Manager
import multiprocessing

def tfidf_creation(text_data, storage_path):

    text_contents = []
    for content in text_data.values():
        text_contents.append(content["content"])
    dct = Dictionary(text_contents)
    dct.save("./tmp.dict")

    tfs = [dct.doc2bow(text) for text in text_contents]
    tf_idf = TfidfModel(tfs, smartirs = "ltn")
    dfs = tf_idf.dfs
    idfs = tf_idf.idfs

    with open("./dfs.json", "w") as f:
        json.dump(dfs, f)
    with open("./idfs.json", "w") as f:
        json.dump(idfs, f)
    
    MmCorpus.serialize("./tmp.mm", tfs)
    tf_idf.save("./tfidf.model")

    return tf_idf

def tfidf_update(new_data, storage_path, obj):

    tf_idf = TfidfModel.load("./tfidf.model")
    
    # if len(deleted_files) ==0 and len(added_files) ==0 and len(modified_files) == 0:
    #     return tf_idf

    tfs = MmCorpus("./tmp.mm")
    dct = Dictionary.load("./tmp.dict")
    
    with open("./dfs.json") as f:
        dfs = json.load(f)
    with open("./idfs.json") as f:
        idfs = json.load(f)
    print(dct.iteritems)
    print(tfs[1][1])

    # update dict first
    for term in new_data[code_file]["content"]:
        if term in dct.token2id:
            tfs[code_file] = 

    # with open(os.path.join(storage_path, obj+"_data.json"), "r") as f:
    #     old_data = json.load(f)
    
    
    
    # # update tfs, df, idf
    # for code_file in modified_files:
    #     if code_file in tfs:
    #         pass
    #     else:
    #         pass 

    # for code_file in modified_files:
    #     code_file = code_file[0]
    #     for term in text_data[code_file]["content"]:
    #         if term in dct
    # for code_file in deleted_files:
        
    # for code_file in modified_files:
        
    # for code_file in added_files:

    # print(tf_idf[tfs[0]])

    