import sys
sys.path.append(".")
from src.tfidf import get_docu_feature,get_term_feature, tfidf_creation
from src.similarity import compute_similarity
from src.similarity import normalization
from src.text_processor import text_processor

def test_compute_similarity():
    code_data = {"/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/StringConstants.java": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/GeneratorSource.java": "what the fucadahfa fafw fawf client googl g", "aa": "I loke igiey RNG"}
    code_data = text_processor(code_data)

    bug_data = {"112": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button"}
    bug_data = text_processor(bug_data)

    word_list, dfs, idfs = get_docu_feature(code_data)

    file_id, code_tfs = get_term_feature(word_list, code_data)

    bug_id, bug_tfs = get_term_feature(word_list, bug_data)
 
    bug_v = tfidf_creation(bug_id, bug_tfs, idfs)
    
    code_v = tfidf_creation(file_id, code_tfs, idfs)
    
    print(compute_similarity(bug_v, code_v, bug_id, file_id))

if __name__=="__main__":

    test_compute_similarity()