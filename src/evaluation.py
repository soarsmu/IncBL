import os

def evaluation(fixed_files, results):

    acc = 0
    map_value = 0

    truth_num = 0
    count = 0
    for bug_id, file_paths in fixed_files.items():
        temp = 0
        map_tmp = 0
        if not len(file_paths) == 0:
            count += 1
            for file_path in file_paths:
                truth_num += 1
                for i in range(results.shape[0]):
                    if results[i]["bug"][0] == bug_id.encode():
                        for j in range(results.shape[1]):
                            if results[i][j]["file"] == file_path.encode():
                                acc += 1
                                temp += 1
                                map_tmp += temp/(j+1.0)

            if not temp == 0:
                map_value += map_tmp / len(file_paths)

    acc /= truth_num
    map_value /= count
    print("The accuracy @ top 10 is", acc)
    print("The MAP @ top 10 is", map_value)