import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET

def bug_reports_division(bug_reports_base, storage_path):

    dir_path = os.walk(bug_reports_base)
    for parent_dir, dir_name, file_names in dir_path:
        
        if file_names[0].split(".")[-1].strip() == "xml":
            if not os.path.exists(os.path.join(storage_path, parent_dir.split("/")[-1].strip())):
                os.makedirs(os.path.join(storage_path, parent_dir.split("/")[-1].strip()))
            all_root = ET.Element("bugrepository", {"name": parent_dir.split("/")[-1].strip()})
            for file_name in file_names:
                tree = ET.parse(os.path.join(parent_dir, file_name))
                root = tree.getroot()
                for child in root:
                    all_root.append(child)
            id_time = []
            all_root[:] = sorted(all_root, key=lambda child: parse(child.get("opendate"), ignoretz=True).isoformat())
            for i, child in enumerate(all_root):
                new_root =  ET.Element(all_root.tag, {"name": parent_dir.split("/")[-1].strip()})
                bug_attrib = child.attrib
                bug_attrib["id"] = str(i+1)
                bug_attrib["opendate"] = str(parse(child.get("opendate"), ignoretz=True))
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
                id_time.append(str(i+1)+".XML"+ "\t" +bug_attrib["opendate"])
            with open(os.path.join(os.path.join(storage_path, parent_dir.split("/")[-1].strip()),"id_time.txt"), "w") as f:
                for line in id_time:
                    f.write(line+"\r\n")

if __name__ == "__main__":
    bug_reports_division("/home/Blinpy-app/evaluation_results/Bugzbook_reports", "/home/Blinpy-app/evaluation_results/splitted_reports")