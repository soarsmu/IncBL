import os
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from src.bug_reader import bug_reader
from src.code_reader import mp_code_reader
from src.tfidf import get_docu_feature, tfidf_creation, update_tfidf_feature
from src.similarity import compute_similarity

class incbl():

    def __init__(self, bug_report_path, code_base_path, file_type, storage_path):
        
        self.bug_report_path = bug_report_path
        self.code_base_path = code_base_path
        self.file_type = file_type
        self.code_storage_path = os.path.join(storage_path, "code/")
        if not os.path.exists(self.code_storage_path):
            os.mkdir(os.path.join(storage_path, "code/"))
        self.bug_storage_path = os.path.join(storage_path, "bugs/")
        if not os.path.exists(self.bug_storage_path):
            os.mkdir(os.path.join(storage_path, "bugs/"))

    def localization(self):
        
        print("bug localization starting...")
        
        start_time = time.time()
        print("read bug reports...")
        bug_data = bug_reader(self.bug_report_path, self.code_base_path, self.file_type, self.bug_storage_path)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("read code files...")
        code_data, added_files, deleted_files, modified_files = mp_code_reader(self.code_base_path, self.file_type, self.code_storage_path)
        print("the time consuming is %f s" %(time.time() - start_time))

        if not os.path.exists(os.path.join(self.code_storage_path, "idfs.npy")):
            start_time = time.time()
            print("get the document-level features...")
            idfs = get_docu_feature(code_data, self.code_storage_path)
            print("the time consuming is %f s" %(time.time() - start_time))

            start_time = time.time()
            print("get the term-level features...")
            bug_vector = tfidf_creation(bug_data, idfs, self.bug_storage_path)
            code_vector = tfidf_creation(code_data, idfs, self.code_storage_path)
            print("the time consuming is %f s" %(time.time() - start_time))
        else: 
            code_vector = update_tfidf_feature(code_data, added_files, deleted_files, modified_files, self.code_storage_path)
            idfs = np.load(os.path.join(self.code_storage_path, "idfs.npy"))
            bug_vector = tfidf_creation(bug_data, idfs, self.bug_storage_path)

        start_time = time.time()
        print("compute similarities...")
        similarity = compute_similarity(bug_vector, code_vector)
        print("the time consuming is %f s" %(time.time() - start_time))
        similarity["score"] = -similarity["score"]
        similarity = np.sort(similarity, order = "score")[:,:9]
        similarity["score"] = -similarity["score"]
        print(similarity)
       
    def evaluation(self):

        acc = 0
        map_value = 0

        truth_num = 0
        count = 0
        for bug_id, file_paths in fixed_files.items():
            temp = 0
            map_tmp = 0
            if not len(file_paths) == 0:
                count += 1
                for file_path in file_paths:
                    truth_num += 1
                    for i in range(results.shape[0]):
                        if results[i]["bug"][0] == bug_id.encode():
                            for j in range(results.shape[1]):
                                if results[i][j]["file"] == file_path.encode():
                                    acc += 1
                                    temp += 1
                                    map_tmp += temp/(j+1.0)

                if not temp == 0:
                    map_value += map_tmp / len(file_paths)

        acc /= truth_num
        map_value /= count
        print("The accuracy @ top 10 is", acc)
        print("The MAP @ top 10 is", map_value)

