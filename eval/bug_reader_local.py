"""
Read locally stored bug reports and preprocess their text
"""

import os
import re
import time
import numpy as np
import xml.etree.ElementTree as ET
from src.text_processor import tokenizer

def bug_reader(bug_reports_path: str):
    """
    Parse bug reports in ".xml" file format, such as Bugzbook dataset.
    """

    bug_data = {}
    fixed_files = {}
    
    
    tree = ET.parse(bug_reports_path)
    root = tree.getroot()
    for child in root[0].findall("buginformation"):
        print(child.tag)
        print(child.find("summary").text)
        print(child.findall("description"))
        

    return bug_data, fixed_files
