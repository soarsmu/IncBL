import sys
sys.path.append(".")
import numpy as np
from src.text_processor import text_processor
from scipy.sparse import dok_matrix
import scipy.io
import scipy
from src.tf_idf_new import tfidf_creation, tfidf_update

def test_tfidf_creation():
    code_data = {"/home/jack/dataset/ZXing/ZXing-1.6/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/StringConstants.java": {"content": ["copyright", "zx", "ing", "author", "licensed", "apache", "license", "version", "license", "file", "compliance", "license", "license", "apache", "license", "license", "require", "applicable", "law", "agree", "write", "software", "distribute", "license", "distribute", "basis", "warranties", "condition", "express", "imply", "license", "specific", "language", "govern", "permission", "limitation", "license", "google", "zxe", "generator", "client", "google", "gwt", "client", "message", "atempt", "localization", "string", "constants", "message", "string", "code", "type", "string", "generate", "button", "string", "constants", "client", "message", "generator", "client", "code", "type", "generate", "button", "zxe", "gwt", "google", "google"], "md5": "2a3d284fd1e906dce4aaa19334c10de1"}, "/home/jack/dataset/ZXing/ZXing-1.6/zxing.appspot/generator/src/com/google/zxing/web/generator/client/StringConstants.java": {"content": ["google", "zxe", "generator", "client", "google", "gwt", "client", "message", "atempt", "localization", "string", "constants", "message", "string", "code", "type", "string", "generate", "button", "string", "constants", "client", "message", "generator", "client", "code", "type", "generate", "button", "zxe", "gwt", "google", "google"], "md5": "2a3d284fd1e906dce4aaa19334c10de1"}}

    tfidf_creation(code_data, "")
    tfidf_update(code_data, "", "")

if __name__=="__main__":

    test_tfidf_creation()