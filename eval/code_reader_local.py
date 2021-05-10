"""
Read locally stored code files and preprocess their text
"""

from src.text_processor import tokenizer
from src.code_parser import parser

def code_reader(code_base_path: str):
    """
    read code files and process code files
    """

    code_data = {}
    with open()