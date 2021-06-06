import os
import json

def evaluation(results, all_res, bug_data, storage_path):
    
    map_value = 0
    map_value_all = 0
    ap_value = {}
    count = 0

    for bug_id, bug_cont in bug_data.items():
        temp1 = 0
        temp2 = 0
        ap_tmp = 0
        all_ap_tmp = 0
        file_paths = bug_cont["fixed_files"]
        if not len(file_paths) == 0:
            count += 1
            ap_value[bug_id] = {}
            for file_path in file_paths:
                for i in range(results.shape[0]):
                    if results[i]["bug"][0] == bug_id.encode():
                        for j in range(results.shape[1]):
                            if results[i][j]["file"] == file_path.encode():
                                temp1 += 1
                                ap_tmp += temp1/(j+1.0)
                
                for i in range(all_res.shape[0]):
                    if all_res[i]["bug"][0] == bug_id.encode():
                        for j in range(all_res.shape[1]):
                            if all_res[i][j]["file"] == file_path.encode():
                                temp2 += 1
                                all_ap_tmp += temp2/(j+1.0)
            print(all_ap_tmp)
            ap_value[bug_id]["AP@top10"] = ap_tmp / len(file_paths)
            ap_value[bug_id]["AP@all"] = all_ap_tmp / len(file_paths)
    
    past_ap_value = {}
    if os.path.exists(os.path.join(storage_path, "evaluation.json")):
        with open(os.path.join(storage_path, "evaluation.json"), "r") as f:
            past_ap_value = json.load(f)
    past_ap_value.update(ap_value)
    
    with open(os.path.join(storage_path, "evaluation.json"), "w") as f:
        json.dump(past_ap_value, f)
    
    if not count ==0:
        for ap in ap_value.values():
            map_value_all += ap["AP@all"]
            map_value += ap["AP@top10"]
    else:
        map_value = 0
        map_value_all = 0

    print("The MAP @ top 10 is", map_value/count)
    print("The MAP @ all results is", map_value_all/count)