"""
Read local code files/github repos, commits and preprocess their text
"""

from tree_sitter import Language, Parser
from src.text_processor import text_processor
from multiprocessing import Pool, Process, Queue, Manager

def code_reader(code_base_path: str) -> dict:
    """
    read code files and process code files

    Args: string, local code store path

    Returns: dict, {path: code content}
    """

    code_data = {}
    
    with open(code_base_path) as f:
        try:
            file_name = code_base_path
            code_data[file_name] = f.read().strip().lower()
        except UnicodeDecodeError:
            return None

        code_data = text_processor(code_data)

        return code_data


# Language.build_library(
#     # Store the library in the `build` directory
#     './build/my-languages.so',

#     # Include one or more languages, need to clone the existing language repos from https://github.com/tree-sitter
#     [
#         '/home/jack/tree-sitter-bash',
#         '/home/jack/tree-sitter-python',
#         '/home/jack/tree-sitter-java',
#         '/home/jack/tree-sitter-c'

#     ]
# )

BASH_LANGUAGE = Language('./build/my-languages.so', 'bash')
PY_LANGUAGE = Language('./build/my-languages.so', 'python')
JAVA_LANGUAGE = Language('./build/my-languages.so', 'java')
C_LANGUAGE = Language('./build/my-languages.so', 'c')
CPP_LANGUAGE = Language('./build/my-languages.so', 'c++')

parser_java = Parser()
parser_java.set_language(JAVA_LANGUAGE)

parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)


# parser_list = {
#     'py':PY_LANGUAGE,
#     'java':JAVA_LANGUAGE,
#     # can be added more
# }

def code_parser():
    """
    parser code to get identifiers and methods

    Args: string, raw code content

    Returns: string
    """
    pass

def changed_code_reader():
    """
    for local evaluation, detect changed file and read it
    
    Args: string, local code store path

    Returns: dict, {path: code content}
    """
    pass
