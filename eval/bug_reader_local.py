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
    print(root[0][0].tag, root[0][0].)
    
    

    return bug_data, fixed_files
