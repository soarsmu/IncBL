import sys
sys.path.append(".")
from src.code_reader import mp_code_reader, code_parser, filter_files

def test_code_reader():
    codebase_path = "/home/jack/dataset/ZXing-1.6/bug/src/com/google/zxing/"
    print(filter_files(codebase_path, ["java"]))

if __name__ == "__main__":

    test_code_reader()
    