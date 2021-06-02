import os
from hashlib import md5
from tree_sitter import Language, Parser
import multiprocessing as mp
from src.utils import db
from src.text_processor import text_processor

def code_reader(code_file, file_type):
    
    code_data = {}

    with open(code_file) as f:
        if f.read(1):
            code_cont = f.read()
            md5_val = md5(code_cont.encode()).hexdigest()

            if db.find({"md5": str(md5_val)}).count() == 0:
                db.remove({"file_path": code_file})
                code_data[code_file] = code_parser(code_cont, file_type)
                code_data = text_processor(code_data)
                db.insert_one({"file_path": code_file, "file_content": code_data[code_file], "md5": str(md5_val)})
    
    return code_data

def mp_code_reader(code_base_path, file_type):

    code_data = {}
    
    code_files = filter_files(code_base_path, file_type)
    print(code_files)
    pool = mp.Pool(mp.cpu_count())
    for code_file in code_files:
        pool.apply_async(code_reader, args=(code_file[0], code_file[1]), callback=code_data.update)
        
    pool.close()
    pool.join()

    return code_data

def filter_files(code_base_path, file_type):

    for res in db.find({}, {"file_path": 1}):
        if not os.path.exists(res["file_path"]):
            db.remove({"file_path": res["file_path"]})

    filtered_files = []
    code_files = []

    dir_path = os.walk(code_base_path)
    for parent_dir, dir_name, file_names in dir_path:
        for file_name in file_names:
            if file_name.split(".")[-1].strip() in file_type:
                code_files.append(os.path.join(parent_dir, file_name))

    for res in db.find({}, {"file_path": 1}):
        if not res["file_path"] in code_files:
            db.remove({"file_path": res["file_path"]})

    for code_file in code_files:
        if db.find({"file_path": code_file}).count() == 0:
            filtered_files.append([code_file, code_file.split(".")[-1].strip()])

    return filtered_files

def code_parser(code_cont, file_type):

    if file_type == "py":
        file_type = "python"
    
    parser = Parser()
    parser.set_language(Language('./lib/languages.so', file_type))

    parsed_code = str.encode(code_cont)
    tree = parser.parse(parsed_code)
    code_lines = code_cont.split('\n')

    identifier = ""
    nodes = [tree.root_node]
    while nodes:
        temp = []
        for node in nodes:
            for child in node.children:
                temp.append(child)
                if(child.type == "identifier"):
                    identifier += code_lines[child.start_point[0]][child.start_point[1]:child.end_point[1]] + " "
        nodes = temp

    return code_cont + identifier
