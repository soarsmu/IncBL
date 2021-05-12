# TODO: 

from src.bug_reader import bug_reader, bug_reader_local
from src.code_reader import code_reader
from src.indexer import index_creation
from src.idf import idf_computing
from src.similarity import compute_bugs_simi, compute_similarity, normalization

class incbl():

    def __init__(self, bug_reports_path, code_base_path, index_path, model_path, fixed_bugs_path):
        """
        read bug reports and code
        read index and model if have
        read fixed_bugs
        """
        if(): # local evaluation
            self.bug_data, self.fixed_files = bug_reader_local(bug_reports_path)
        else: 
            self.bug_data = bug_reader(bug_reports_path)
        
        if(): # first use
            self.index = index_creation()
            self.model = idf_computing()
        else:
            self.index = index_path
            self.model = model_path
        
        self.fixed_bugs = fixed_bugs_path
        self.code_data = code_reader(code_base_path)
        
            
    def index_update(self):
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

    # TODO: This can seen as query part
    def localization(self):
        """
        query part
        
        Args: index, model

        Returns: dict, {ID: path}
        """

        compute_bugs_simi()
        normalization()
        compute_similarity()

        pass

    def evaluation(self):
        """
        computing the MAP, ACC, MRR values if have ground truth

        Args: two dict, {ID: results}, {ID: fixed files} 

        Returns: numbers, MAP, ACC, MRR values
        """
        pass