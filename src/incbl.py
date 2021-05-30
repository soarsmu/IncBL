import os
import time
import numpy as np
from src.bug_reader import bug_reader_local
from src.code_reader import code_reader
from src.tfidf import get_docu_feature, get_term_feature, tfidf_creation
from src.similarity import compute_similarity, normalization, combine_bugs_simi
from src.evaluation import evaluation

class incbl():

    def __init__(self, bug_report_path, code_base_path, file_extension):
        """
        read bug reports and code
        read index and model if have
        read fixed_bugs
        """
        self.bug_report_path = bug_report_path
        self.code_base_path = code_base_path
        self.file_extension = file_extension
        self.results = {}

    def localization(self):
        """
        query part
        
        Args: index, model

        Returns: dict, {ID: path}
        """
        print("\n localization starting...\n")
        start_time = time.time()

        bug_data, fixed_files = bug_reader_local(self.bug_report_path, self.code_base_path, self.file_extension)
        code_data, code_length = code_reader(self.code_base_path, self.file_extension)
        word_list, dfs, idfs = get_docu_feature(code_data)

        file_id, code_tfs = get_term_feature(word_list, code_data)

        bug_id, bug_tfs = get_term_feature(word_list, bug_data)
    
        bug_v = tfidf_creation(bug_id, bug_tfs, idfs)
        
        code_v = tfidf_creation(file_id, code_tfs, idfs)

        similarity = compute_similarity(bug_v, code_v, bug_id, file_id)

        similarity = normalization(similarity, code_length, bug_id, file_id)
        
        similarity = combine_bugs_simi(similarity, fixed_files, bug_data, bug_id, file_id)
        print(similarity)
        ranks = np.argsort(similarity, axis =0)
        for i in ranks:
            print(i)
        
        #similarity = normalization(compute_similarity(bug_data, code_data, dct, model), code_length)
        
        #self.results = combine_bugs_simi(similarity, fixed_files, bug_data, self.code_base_path)

        # print("the time overhead is ", time.time()-start_time, "\n The results is\n")

        # for bug_id, code_files in self.results.items():
        #     print(bug_id + ":" + "\n")
        #     index = 0
        #     print(fixed_files[bug_id])
        #     for code_path, simi_score in code_files.items():
        #         if not index >= 10:
        #             print("\t" + code_path + "\t" + str(simi_score))
        #             index += 1
        #         else: break
        
        # evaluation(bug_data, fixed_files, self.code_base_path, self.results)

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
