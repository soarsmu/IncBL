import sys
sys.path.append(".")
from src.text_processor import text_processor
from src.code_reader import code_reader

def test_code_reader():
    codebase_path = "/home/jack/Blinpy-app/src"

    print(code_reader(codebase_path, ["py"]))


if __name__ == "__main__":

    test_code_reader()