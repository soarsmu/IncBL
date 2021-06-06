import os
import json

def evaluation(results, bug_data, storage_path):
    
    acc = 0
    map_value = 0
    ap_value = {}
    truth_num = 0
    count = 0

    for bug_id, bug_cont in bug_data.items():
        temp_1 = 0
        temp_2 = 0
        map_tmp = 0
        file_paths = bug_cont["fixed_files"]
        if not len(file_paths) == 0:
            count += 1
            for file_path in file_paths:
                truth_num += 1
                for i in range(results.shape[0]):
                    if results[i]["bug"][0] == bug_id.encode():
                        temp_1 += 1
                        for j in range(results.shape[1]):
                            if results[i][j]["file"] == file_path.encode():
                                temp_2 += 1
                                map_tmp += temp_2/(j+1.0)
            if temp_1 > 0:
                acc += 1
                temp_1 = 0
            if not temp_2 == 0:
                ap_value[bug_id] = map_tmp / len(file_paths)
    
    past_ap_value = {}
    if os.path.exists(os.path.join(storage_path, "evaluation.json")):
        with open(os.path.join(storage_path, "evaluation.json"), "r") as f:
            past_ap_value = json.load(f)
    past_ap_value.update(ap_value)
    
    with open(os.path.join(storage_path, "evaluation.json"), "w") as f:
        json.dump(past_ap_value, f)
    
    acc /= len(bug_data)
    if not count ==0:
        map_value = sum(list(ap_value.values()))/count
    else:
        map_value = 0
    print("The accuracy @ top 10 is", acc)
    print("The MAP @ top 10 is", map_value)