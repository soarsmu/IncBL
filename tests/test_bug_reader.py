import sys
sys.path.append(".")
from src.bug_reader import bug_reader

def test_bug_reader():
    
    print(bug_reader("/home/jack/dataset/Bugzbook/tika/0.8.xml", "/home/jack/dataset/tika-1.20", ["java"]))

if __name__ == "__main__":
    test_bug_reader()