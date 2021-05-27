import os
import time
from src.bug_reader import bug_reader_local
from src.code_reader import code_reader
from src.tfidf import tfidf_computing
from src.similarity import compute_similarity, normalization

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

        # TODO: history info and normalization
        bug_data, fixed_files = bug_reader_local(self.bug_report_path)
        code_data, code_length = code_reader(self.code_base_path, self.file_extension)
        code_data, dct, model = tfidf_computing(code_data)

        self.results = normalization(compute_similarity(bug_data, code_data, dct, model), code_length)
        
        print("the time overhead is ", time.time()-start_time, "\n The results is\n")

        for bug_id, code_paths in self.results.items():
            print(bug_id + ":" + "\n")
            for code_path in code_paths:
                if code_path[1] >= 0.15:
                    print("\t" + code_path[0] + "\t" + str(code_path[1]))

    def evaluation(self):
        """
        computing the MAP, ACC, MRR values if have ground truth

        Args: two dict, {ID: results}, {ID: fixed files} 

        Returns: numbers, MAP, ACC, MRR values
        """
        print("\n evaluation starting...\n")
        bug_data, fixed_files = bug_reader_local(self.bug_report_path)
        acc = 0
        map_value = 0

        truth_num = 0
        for bug_id, file_paths in fixed_files.items():
            temp = 0
            map_tmp = 0
            for file_path in file_paths:
                truth_num += 1
                file_path = os.path.join(self.code_base_path, file_path)
                for i, result in enumerate(self.results[bug_id]):
                    if result[0] == file_path and i < 10:
                        acc +=1

                        temp += 1
                        map_tmp += temp/(i+1.0)

            if not temp == 0:
                map_value += map_tmp / temp 

        acc /= truth_num
        map_value /= len(fixed_files)
        print("\t The accuracy @ top 10 is", acc, "\n", "\t The MAP @ top 10 is", map_value)
                    


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
