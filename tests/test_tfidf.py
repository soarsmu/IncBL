import sys
sys.path.append(".")
from src.tfidf import tfidf_creation, get_docu_feature, get_term_feature
from src.text_processor import text_processor

def test_tfidf_creation():
    code_data = {"/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/StringConstants.java": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/GeneratorSource.java": "what the fucadahfa fafw fawf client googl g", "awawwwwa": "I loke igiey awawdawdawG"}
    code_data = text_processor(code_data)
    bug_data = {"112": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "1aw12": "I loke igiey awawdawdaw"}
    bug_data = text_processor(bug_data)
    idfs = get_docu_feature(code_data)
    
    tf_idfs = tfidf_creation(bug_data, idfs)

    print(tf_idfs)
    

if __name__=="__main__":

    test_tfidf_creation()