import os
import time
from tree_sitter import Language, Parser
from multiprocessing import Queue, Pool, Manager
from src.text_processor import text_processor

def code_reader(code_file, file_type, q):
    
    code_data = {}
    with open(code_file) as f:
        if f.read(1):
            code_data[code_file] = code_parser(f.read(), file_type)
    code_data = text_processor(code_data)
    
    q.put(code_data)

def mp_code_reader(code_base_path, file_type):

    code_data = {}
    
    print("\n let's read the code files...\n")
    start_time = time.time()
    code_files = filter_files(code_base_path, file_type)

    q = Manager().Queue()
    pool = Pool(processes=8)
    for code_file in code_files:
        pool.apply_async(code_reader, args=(code_file[0], code_file[1], q))
    pool.close()
    pool.join()

    for code_file in code_files:
        code_data.update(q.get())

    print("the overhead is ", time.time()-start_time)

    return code_data

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


def filter_files(code_base_path, file_type):

    code_files = []

    dir_path = os.walk(code_base_path)
    for parent_dir, dir_name, file_names in dir_path:
        for file_name in file_names:
            if(file_name.split(".")[-1].strip() in file_type):
                code_files.append([os.path.join(parent_dir, file_name), file_name.split(".")[-1].strip()])
    
    return code_files
