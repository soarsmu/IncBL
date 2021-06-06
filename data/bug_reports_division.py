import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET

def bug_reports_division(bug_reports_base, storage_path):

    dir_path = os.walk(bug_reports_base)
    for parent_dir, dir_name, file_names in dir_path:
        for file_name in file_names:
            if file_name.split(".")[-1].strip() == "xml":
                if not os.path.exists(os.path.join(storage_path, parent_dir.split("/")[-1].strip())):
                    os.makedirs(os.path.join(storage_path, parent_dir.split("/")[-1].strip()))
                
                tree = ET.parse(os.path.join(parent_dir, file_name))
                root = tree.getroot()
                root[:] = sorted(root, key=lambda child: parse(child.get("opendate"), ignoretz=True).isoformat())

                for i, child in enumerate(root):
                    new_root =  ET.Element(root.tag, {"name": parent_dir.split("/")[-1].strip()})
                    bug_attrib = child.attrib
                    bug_attrib["id"] = str(i+1)
                    bug = ET.SubElement(new_root, "bug", bug_attrib)
                    title = ET.SubElement(bug, "title")
                    if child[0].text:
                        title.text = child[0].text
                    description = ET.SubElement(bug, "description")
                    if child[1].text:
                        description.text = child[1].text
                    fixed_files = ET.SubElement(bug, "fixedfiles")
                    for file_path in child[2].findall("file"):
                        files = ET.SubElement(fixed_files, "file")
                        files.text = file_path.text
                    new_tree = ET.ElementTree(new_root)
                    new_tree.write(os.path.join(os.path.join(storage_path, parent_dir.split("/")[-1].strip()), str(i+1)+".XML"), encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    bug_reports_division("/home/jack/dataset/Bugzbook/Bugzbook", "/home/jack/dataset/Bugzbook/splited_Bugzbook")
    
    # bug_data = {}

    # tree = ET.parse(bug_report_path)
    # root = tree.getroot()
    # for child in root:
    #     if child[1].text:
    #         bug_content = text_processor(child[0].text + child[1].text)
    #     else:
    #         bug_content = text_processor(child[0].text)
    #     fixed_files = []
    #     for file_path in child[2].findall("file"):
    #         if file_path.text.split(".")[-1].strip() in file_type:
    #             fixed_files.append(os.path.join(code_base_path, file_path.text))
    #     open_date = parse(child.get("opendate"), ignoretz=True).isoformat()
    #     bug_data[child.get("id")] = {"content": bug_content, "fixed_files": fixed_files, "open_date": open_date}

    # past_bugs = {}
    # if os.path.exists(os.path.join(storage_path, "bug_data.json")):
    #     with open(os.path.join(storage_path, "bug_data.json"), "r") as f:
    #         past_bugs = json.load(f)

    # return bug_data, past_bugs