import os
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from src.bug_reader import bug_reader
from src.code_reader import mp_code_reader
from src.tfidf import get_docu_feature, tfidf_creation, update_tfidf_feature
from src.similarity import compute_similarity
from src.evaluation import evaluation

class incbl():

    def __init__(self, bug_report_path, code_base_path, file_type, storage_path, incbl_root):
        
        self.bug_report_path = bug_report_path
        self.code_base_path = code_base_path
        self.file_type = file_type
        self.storage_path = os.path.join(storage_path)
        self.code_storage_path = os.path.join(storage_path, "code/")
        if not os.path.exists(self.code_storage_path):
            os.mkdir(os.path.join(storage_path, "code/"))
        self.bug_storage_path = os.path.join(storage_path, "bugs/")
        if not os.path.exists(self.bug_storage_path):
            os.mkdir(os.path.join(storage_path, "bugs/"))
        self.incbl_root = incbl_root
        self.results = {}

    def localization(self):
        
        print("bug localization starting...")
        
        start_time = time.time()
        print("read bug reports...")
        bug_data, past_bugs = bug_reader(self.bug_report_path, self.code_base_path, self.file_type, self.bug_storage_path)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("read code files...")
        code_data, added_files, deleted_files, modified_files = mp_code_reader(self.code_base_path, self.file_type, self.code_storage_path, self.incbl_root)
        print("the time consuming is %f s" %(time.time() - start_time))

        if not os.path.exists(os.path.join(self.code_storage_path, "idfs.npy")):
            start_time = time.time()
            print("get the document-level features for code files...")
            idfs = get_docu_feature(code_data, self.code_storage_path, True)
            print("the time consuming is %f s" %(time.time() - start_time))

            start_time = time.time()
            print("get the term-level features...")
            bug_vector = tfidf_creation(bug_data, idfs, self.bug_storage_path, False)
            code_vector = tfidf_creation(code_data, idfs, self.code_storage_path, True)
            print("the time consuming is %f s" %(time.time() - start_time))
        elif len(added_files + modified_files) > 20:
            start_time = time.time()
            print("get the document-level features for code files...")
            idfs = get_docu_feature(code_data, self.code_storage_path, True)
            print("the time consuming is %f s" %(time.time() - start_time))

            start_time = time.time()
            print("get the term-level features...")
            bug_vector = tfidf_creation(bug_data, idfs, self.bug_storage_path, False)
            code_vector = tfidf_creation(code_data, idfs, self.code_storage_path, True)
            print("the time consuming is %f s" %(time.time() - start_time))
        else:
            start_time = time.time()
            print("update tfidf model...")
            code_vector = update_tfidf_feature(code_data, added_files, deleted_files, modified_files, self.code_storage_path)
            print("the time consuming is %f s" %(time.time() - start_time))

            idfs = np.load(os.path.join(self.code_storage_path, "idfs.npy"))
            bug_vector = tfidf_creation(bug_data, idfs, self.bug_storage_path, False)

        start_time = time.time()
        print("compute similarities...")
        similarity = compute_similarity(bug_vector, code_vector, bug_data, past_bugs, self.bug_storage_path)
        print("the time consuming is %f s" %(time.time() - start_time))
        similarity["score"] = -similarity["score"]
        results = np.sort(similarity, order = "score")[:,:10]
        similarity = np.sort(similarity, order = "score")
        similarity["score"] = -similarity["score"]
        self.results = results
        for i in range(self.results.shape[0]):
            for j in range(self.results.shape[1]):
                print(j+1, ": ", self.results[i][j]["file"].decode())
        # evaluation(self.results, similarity, bug_data, self.storage_path)
