import os
import json
import multiprocessing

from hashlib import md5
from multiprocessing import Pool, Queue, Manager
from tree_sitter import Language, Parser
from src.text_processor import text_processor

manager = Manager()
q_to_store = manager.Queue()

def mp_code_reader(code_base_path, file_type, storage_path, incbl_root):

    update_files = filter_files(code_base_path, file_type, storage_path)

    # if os.path.exists(os.path.join(storage_path, "code_data.json")):
    #     with open(os.path.join(storage_path, "code_data.json"), "r") as f:
    #         code_data = json.load(f)
    # else:
    new_code_data = {}

    if len(update_files):
        pool = Pool(multiprocessing.cpu_count())
        for code_file in update_files:
            pool.apply_async(code_files_reader, args=(code_file[0], code_file[1], incbl_root))
        pool.close()
        pool.join()

    while not q_to_store.empty():
        single_data = q_to_store.get()
        try:
            file_name = list(single_data.keys())[0]
        except:
            continue
        if file_name:
            new_code_data[file_name] = single_data.values()
    
    # with open(os.path.join(storage_path, "code_data.json"), "w") as f:
    #     json.dump(code_data, f)
    
    return new_code_data

def filter_files(code_base_path, file_type, storage_path):

    code_files = []
    update_files = []
    
    dir_path = os.walk(code_base_path)
    for parent_dir, dir_name, file_names in dir_path:
        for file_name in file_names:
            if file_name.split(".")[-1].strip() in file_type:
                code_files.append(os.path.join(parent_dir, file_name))
    
    if os.path.exists(os.path.join(storage_path, "code_data.json")):
        with open(os.path.join(storage_path, "code_data.json"), "r") as f:
            code_data = json.load(f)

            for file_path in list(code_data.keys()):
                if not file_path in code_files:
                    update_files.append(file_path)

            for code_file in code_files:

                if os.path.getsize(code_file) and not code_file in code_data.keys():
                    update_files.append([code_file, code_file.split(".")[-1].strip()])

                elif os.path.getsize(code_file):
                    code_cont = open(code_file)
                    md5_val = md5(code_cont.read().encode()).hexdigest()
                    code_cont.close()
                    if not md5_val == code_data[code_file]["md5"]:
                        update_files.append([code_file, code_file.split(".")[-1].strip()])

    else:
        for code_file in code_files:
            update_files.append([code_file, code_file.split(".")[-1].strip()])

    return update_files

def code_files_reader(code_file, file_type, incbl_root):
    code_data = {}

    with open(code_file) as f:
        if os.path.getsize(code_file):
            code_cont = f.read()
            md5_val = md5(code_cont.encode()).hexdigest()
            cont = text_processor(code_parser(code_cont, file_type, incbl_root))
            code_data[code_file] = {"content": cont, "md5": md5_val}

    q_to_store.put(code_data)

def code_parser(code_cont, file_type, incbl_root):

    if file_type == "py":
        file_type = "python"
    
    parser = Parser()
    parser.set_language(Language(os.path.join(incbl_root, "lib/languages.so"), file_type))
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
