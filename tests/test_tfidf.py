import sys
sys.path.append(".")
import numpy as np
from src.tfidf import tfidf_creation, get_docu_feature, get_term_feature
from src.text_processor import text_processor

def test_tfidf_creation():
    
    print(np.load("./data/jack-zxing/code/idfs.npy"))

if __name__=="__main__":

    test_tfidf_creation()