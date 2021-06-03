import os
import argparse
import pymongo
from src.incbl import incbl

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="A incremental bug localization tool")
    parser.add_argument("user_name", help="tool user's name")
    parser.add_argument("repo_name", help="deployed repo name")
    parser.add_argument("bug_report_path", help="Bug report path")
    parser.add_argument("code_base_path", help="Codebase directory")
    parser.add_argument("-ft", "--file_type", nargs="+", help="Suffixes of files to be processed", default=["java"])
    parser.add_argument("-sp", "--storage_path", nargs="?", help="storage intermediate file", default="")
    args = parser.parse_args()
    user_name = args.user_name
    repo_name = args.repo_name
    if args.storage_path == "":
        storage_path = os.path.join("./data", str(user_name+"-"+repo_name))
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

    bug_report_path = args.bug_report_path
    code_base_path = args.code_base_path
    file_type = args.file_type
    incbl = incbl(bug_report_path, code_base_path, file_type, storage_path)
    incbl.localization()


