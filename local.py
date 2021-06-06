import os
import argparse
from src.incbl import incbl

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="A incremental bug localization tool")
    parser.add_argument("bug_report_path", help="Bug report path")
    parser.add_argument("code_base_path", help="Codebase directory")
    parser.add_argument("repo_name", help="repositary name")
    parser.add_argument("-ft", "--file_type", nargs="+", help="Suffixes of files to be processed", default=["java", "py", "c", "cpp"])
    parser.add_argument("-sp", "--storage_path", nargs="?", help="storage intermediate file", default="")
    args = parser.parse_args()

    bug_report_path = args.bug_report_path
    code_base_path = args.code_base_path
    repo_name = args.repo_name
    file_type = args.file_type
    if args.storage_path == "":
        storage_path = "/home/jack/eval/"+ repo_name +"/.incbl-data"
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    incbl = incbl(bug_report_path, code_base_path, file_type, storage_path)
    incbl.localization()


