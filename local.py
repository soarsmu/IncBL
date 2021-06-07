import os
import argparse
from src.incbl import incbl

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="A incremental bug localization tool")
    parser.add_argument("incbl_root", help = "root")
    parser.add_argument("bug_report_path", help="Bug report path")
    parser.add_argument("code_base_path", help="Codebase directory")
    parser.add_argument("-ft", "--file_type", nargs="+", help="Suffixes of files to be processed", default=["java", "py", "c", "cpp"])
    parser.add_argument("-sp", "--storage_path", nargs="?", help="storage intermediate file", default="")
    args = parser.parse_args()

    incbl_root = args.incbl_root
    bug_report_path = args.bug_report_path
    code_base_path = args.code_base_path
    file_type = args.file_type
    if args.storage_path == "":
        storage_path = os.path.join(incbl_root, ".incbl-data" + code_base_path.split("/")[-1])
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    incbl = incbl(bug_report_path, code_base_path, file_type, storage_path, incbl_root)
    incbl.localization()


