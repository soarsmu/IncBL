"""
Read bug reports/issues and preprocess their text
"""

import xml.etree.ElementTree as ET
from src.text_processor import text_processor

def bug_reader_local(bug_reports_path: str):
    """
    Parse bug reports in ".xml" file format, such as Bugzbook dataset.

    Args: local bug reports store path

    Returns: two dict, {ID: bug information}, {ID: fixed files}
    """

    bug_data = {}
    fixed_files = {}

    tree = ET.parse(bug_reports_path)
    root = tree.getroot()
    for child in root:
        bug_data[child.get("id")] = child[0].find("summary").text + child[0].find("description").text
        fixed_files[child.get("id")] = child[1].find("file").text    
    bug_data = text_processor(bug_data)
    return bug_data, fixed_files

# TODO: access github to get issues' content


def bug_reader(bug_reports_path: str):
    """
    Parse bug reports in json data format from github

    Args: json data from github

    Returns: one dict, {ID: bug information}
    """

    pass
