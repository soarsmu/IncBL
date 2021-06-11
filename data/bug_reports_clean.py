import os
from dateutil.parser import parse
import xml.etree.ElementTree as ET

from numpy.core.fromnumeric import sort

def bug_reports_division(bug_reports_base, storage_path, file_type):
    remove_truth = os.path.join(storage_path, "remove_truth")
    if not os.path.exists(remove_truth):
        os.makedirs(remove_truth)
    remove_reports = os.path.join(storage_path, "remove_reports")
    if not os.path.exists(remove_reports):
        os.makedirs(remove_reports)

    dir_path = os.walk(bug_reports_base)
    for parent_dir, dir_name, file_names in dir_path:
        file_names = sorted(file_names)
        # print(file_names)
        if file_names[0].split(".")[-1].strip() == "xml":
            if not os.path.exists(os.path.join(remove_truth, parent_dir.split("/")[-1].strip())):
                os.makedirs(os.path.join(remove_truth, parent_dir.split("/")[-1].strip()))
            if not os.path.exists(os.path.join(remove_reports, parent_dir.split("/")[-1].strip())):
                os.makedirs(os.path.join(remove_reports, parent_dir.split("/")[-1].strip()))
            ver_time1 = []
            for file_name in file_names:
                all_root = ET.Element("bugrepository", {"name": parent_dir.split("/")[-1].strip()})
                tree = ET.parse(os.path.join(parent_dir, file_name))
                root = tree.getroot()
                for child in root:
                    count = 0
                    if child[2].findall("file"):
                        for file_path in child[2].findall("file"):
                            if file_path.text and not file_path.text.split(".")[-1] in file_type:
                                child[2].remove(file_path)
                            if file_path.text and file_path.text.split(".")[-1] in file_type:
                                count += 1
                    if count > 0 :
                        all_root.append(child)
                all_root[:] = sorted(all_root, key=lambda child: parse(child.get("opendate"), ignoretz=True).isoformat())
                count = 0
                for child in all_root:
                    count += 1
                if count > 0:
                    new_tree = ET.ElementTree(all_root)
                    new_tree.write(os.path.join(os.path.join(remove_truth, parent_dir.split("/")[-1].strip()), file_name), encoding="utf-8", xml_declaration=True)
                    ver_time1.append(file_name + "\t" + str(parse(all_root[-1].get("opendate"), ignoretz=True)))
            with open(os.path.join(os.path.join(remove_truth, parent_dir.split("/")[-1].strip()),"ver_time.txt"), "w") as f:
                for line in ver_time1:
                    f.write(line+"\r\n")
            ver_time2 = []
            for file_name in file_names:
                all_root = ET.Element("bugrepository", {"name": parent_dir.split("/")[-1].strip()})
                tree = ET.parse(os.path.join(parent_dir, file_name))
                root = tree.getroot()
                for child in root:
                    count = 1
                    if child[2].findall("file"):
                        for file_path in child[2].findall("file"):
                            if child[2].findall("file"):
                                for file_path in child[2].findall("file"):
                                    if not file_path.text:
                                        count = 0
                                    if file_path.text and not file_path.text.split(".")[-1] in file_type:
                                        count = 0
                            else:
                                count = 0
                    if count == 1 :
                        all_root.append(child)
                all_root[:] = sorted(all_root, key=lambda child: parse(child.get("opendate"), ignoretz=True).isoformat())
                count = 0
                for child in all_root:
                    count += 1
                if count > 0:
                    new_tree = ET.ElementTree(all_root)
                    new_tree.write(os.path.join(os.path.join(remove_reports, parent_dir.split("/")[-1].strip()), file_name), encoding="utf-8", xml_declaration=True)
                    ver_time2.append(file_name + "\t" + str(parse(all_root[-1].get("opendate"), ignoretz=True)))
            with open(os.path.join(os.path.join(remove_reports, parent_dir.split("/")[-1].strip()),"ver_time.txt"), "w") as f:
                for line in ver_time2:
                    f.write(line+"\r\n")
if __name__ == "__main__":
    bug_reports_division("/home/jack/dataset/Bugzbook/Bugzbook", "/home/jack/clean_bugzbook", ["java", "py", "c", "cpp"])