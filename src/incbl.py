import os
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from src.bug_reader import bug_reader
from src.code_reader import mp_code_reader
from src.tfidf import get_docu_feature, get_term_feature, tfidf_creation
from src.similarity import compute_similarity
from src.evaluation import evaluation

class incbl():

    def __init__(self, bug_report_path, code_base_path, file_type):
        
        self.bug_report_path = bug_report_path
        self.code_base_path = code_base_path
        self.file_type = file_type

    def localization(self):
        
        print("bug localization starting...")
        
        start_time = time.time()
        print("read bug reports...")
        bug_data, fixed_files = bug_reader(self.bug_report_path, self.code_base_path, self.file_type)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("read code files...")
        code_data = mp_code_reader(self.code_base_path, self.file_type)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("get the document-level features...")
        idfs = get_docu_feature(code_data)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("get the term-level features...")
        bug_vector = tfidf_creation(bug_data, idfs)
        code_vector = tfidf_creation(code_data, idfs)
        print("the time consuming is %f s" %(time.time() - start_time))
        
        start_time = time.time()
        print("compute similarities...")
        similarity = compute_similarity(bug_vector, code_vector)
        print("the time consuming is %f s" %(time.time() - start_time))
        similarity["score"] = -similarity["score"]
        similarity = np.sort(similarity, order = "score")[:,:9]
        similarity["score"] = -similarity["score"]
        print(similarity)
        
        print("evaluation start...")
        evaluation(fixed_files, similarity)

       
    def tf_update(self):
        """
        update index matrices

        Args: two dict, {path, code content}, {path, index}
        """
        pass

    def idf_update(self):
        """
        update index matrices

        Args: two dict, {path, code content}, {path, index}
        """
        pass

    def fixed_bugs_update(self):
        """
        save/update fixed bugs as .npy file
        
        """
        pass
