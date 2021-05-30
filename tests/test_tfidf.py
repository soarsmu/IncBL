import sys
sys.path.append(".")
from src.tfidf import tfidf_creation
from src.text_processor import text_processor

def test_tfidf_creation():
    code_data = {"/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/StringConstants.java": "googl zxing web gener client googl zxing web gener client googl gwt client messag atempt local constant messag code type gener button", "/zxing.appspot.com/generator/src/com/google/zxing/web/generator/client/GeneratorSource.java": "googl zxing web gener client googl zxing web gener client googl gwt user client ui grid googl gwt user client ui widget gener sourc grid widget text gener valid widget widget gener set focu"}
    code_data = text_processor(code_data)

    expected_result = {}

    file_id, tf_idfs = tfidf_creation(code_data)

    print(tf_idfs)
    

if __name__=="__main__":

    test_tfidf_creation()