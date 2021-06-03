import os
import json
import xml.etree.ElementTree as ET
from src.text_processor import text_processor

def bug_reader(bug_report_path, code_base_path, file_type, storage_path):
  
    bug_data = {}

    tree = ET.parse(bug_report_path)
    root = tree.getroot()
    for child in root:
        if child[1].text:
            bug_content = text_processor(child[0].text + child[1].text)
        else:
            bug_content = text_processor(child[0].text)
        fixed_files = []
        for file_path in child[2].findall("file"):
            if file_path.text.split(".")[-1].strip() in file_type:
                fixed_files.append(os.path.join(code_base_path, file_path.text))
        bug_data[child.get("id")] = {"bug_content": bug_content, "fixed_files": fixed_files}
        
    with open(os.path.join(storage_path + "bug_data.json"), "a") as f:
        json.dump(bug_data, f, sort_keys=True)

    return bug_data
