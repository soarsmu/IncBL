import sys
sys.path.append(".")
from src.tfidf import get_docu_feature, get_term_feature,  tfidf_creation
from src.similarity import compute_similarity
from src.text_processor import text_processor

def test_compute_similarity():
    code_data = {"/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/StringConstants.java": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/GeneratorSource.java": "what the fucadahfa fafw fawf client googl g", "awawwwwa": "I loke igiey awawdawdaw"}

    code_data = text_processor(code_data)

    bug_data = {"112": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "1aw12": "I loke igiey awawdawdaw"}
    bug_data = text_processor(bug_data)
    
    idfs = get_docu_feature(code_data)

    bug_v = tfidf_creation(bug_data, idfs)
    code_v = tfidf_creation(code_data, idfs)
    
    print(compute_similarity(bug_v, code_v))

if __name__=="__main__":

    test_compute_similarity()