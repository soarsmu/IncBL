"""
Read locally stored code files and preprocess their text
"""

from src.text_processor import tokenizer
# from src.code_parser import parser

def code_reader(code_base_path: str):
    """
    read code files and process code files
    """

    code_data = {}

    with open(code_base_path) as f:
        try:
            file_name = code_base_path
            code_data[file_name] = f.read().strip().lower()
        except UnicodeDecodeError:
            return None

        code_data = tokenizer(code_data)

        return code_data

