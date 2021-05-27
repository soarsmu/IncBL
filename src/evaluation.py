import os

def evaluation(bug_data:dict, fixed_files:dict, code_base_path:str, results:dict):
    """
    computing the MAP, ACC, MRR values if have ground truth

    Args: two dict, {ID: results}, {ID: fixed files} 

    Returns: numbers, MAP, ACC, MRR values
    """
    print("\n evaluation starting...\n")
    acc = 0
    map_value = 0

    truth_num = 0
    for bug_id, file_paths in fixed_files.items():
        temp = 0
        map_tmp = 0
        for file_path in file_paths:
            truth_num += 1
            for i, result in enumerate(results[bug_id].keys()):
                if result == file_path and i < 10:
                    acc += 1
                    temp += 1
                    map_tmp += temp/(i+1.0)

        if not temp == 0:
            map_value += map_tmp / temp 

    acc /= truth_num
    map_value /= len(fixed_files)
    print("\t The accuracy @ top 10 is", acc, "\n", "\t The MAP @ top 10 is", map_value)