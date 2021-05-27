"""
Read local code files/github repos, commits and preprocess their text
"""
import os
from tree_sitter import Language, Parser
from src.text_processor import text_processor
import time

def code_reader(code_base_path: str, extension: list) -> dict:
    """
    read code files and process code files

    Args: string, local code store path

    Returns: dict, {path: code content}
    """
    code_data = {}
    code_length = {}

    print("\n let's read the code files...\n")
    start_time = time.time()

    dir_path = os.walk(code_base_path)
    for parent_dir, dir_name, file_names in dir_path:
        for file_name in file_names:
            if(file_name.split(".")[-1].strip() in extension):
                code_path = os.path.join(parent_dir, file_name)
                with open(code_path) as f:
                    if f.read(1):
                        code_data[code_path] = code_parser(f.read())

    code_data = text_processor(code_data)

    for code_path, code_cont in code_data.items():
        code_length[code_path] = len(code_cont)

    print("the time overhead is ", time.time()-start_time)

    return code_data, code_length

def code_parser(code_cont: str):
    """
    parser code to get identifiers and methods

    Args: string, raw code content

    Returns: string
    """

    if not os.path.exists("./lib/languages.so"):
        Language.build_library(
            # Store the library in the `lib` directory
            "./lib/languages.so",

            # Attention! Change your own path to include one or more languages, need to clone the existing language repos from https://github.com/tree-sitter
            [
                "/home/jack/tree-sitter-java",
            ]
        )

    # TODO: This part needs to be writen more clear.
    JAVA_LANGUAGE = Language('./lib/languages.so', 'java')
    parser_java = Parser()
    parser_java.set_language(JAVA_LANGUAGE)
    parsed_code = str.encode(code_cont)
    tree = parser_java.parse(parsed_code)
    
    cursor = tree.walk()
    index = cursor.node.child_count
    code_content_lines = code_cont.split('\n')
    names = []
    cursor.goto_first_child()
    while not index == 0:
        if(cursor.node.type == 'package_declaration'):
            names.append(code_content_lines[cursor.node.start_point[0]][cursor.node.start_point[1]:cursor.node.end_point[1]])
        if(cursor.node.type == 'class_declaration'):
            cursor.goto_first_child()
            while cursor.goto_next_sibling():
                if(cursor.node.type == 'identifier'):
                    names.append(code_content_lines[cursor.node.start_point[0]][cursor.node.start_point[1]:cursor.node.end_point[1]])
            cursor.goto_first_child()
            while cursor.goto_next_sibling():
                if(cursor.node.type == 'method_declaration'):
                    cursor.goto_first_child()
                    while cursor.goto_next_sibling():
                        if(cursor.node.type == 'identifier'):
                            names.append(code_content_lines[cursor.node.start_point[0]][cursor.node.start_point[1]:cursor.node.end_point[1]])
                    cursor.goto_parent()
            cursor.goto_parent()
            cursor.goto_parent()
        cursor.goto_next_sibling()
        index -= 1
    return code_cont + str(names)

def changed_code_reader():
    """
    for local evaluation, detect changed file and read it
    
    Args: string, local code store path

    Returns: dict, {path: code content}
    """
    pass
