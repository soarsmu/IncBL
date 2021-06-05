import os
import json
import time 
import numpy as np
from src.tfidf import get_docu_feature, tfidf_creation, update_tfidf_feature

def compute_similarity(bug_vector, code_vector, bug_data, past_bugs, storage_path):

    similarity = np.zeros((bug_vector.shape[0], code_vector.shape[0]), dtype=[("bug", "a30"),("file", "a250"), ("score", "f4")])
    past_bug_vectors, past_bugs = update_bug_tfidf(past_bugs, bug_data, storage_path)

    for i in range(bug_vector.shape[0]):
        similarity[i]["bug"] = bug_vector[i]["id"][0]
        for j in range(code_vector.shape[0]):
            alpha = 0.2
            similarity[i][j]["file"] = code_vector[j]["id"][0]
            similarity[i][j]["score"] = (1 - alpha) * (0.5 + 0.5 * np.sum(bug_vector[i]["tf_idf"] * code_vector[j]["tf_idf"])/(np.linalg.norm(bug_vector[i]["tf_idf"]) * np.linalg.norm(code_vector[j]["tf_idf"]))) * code_vector[j]["norm"][0] + alpha * computing_bug_simi(past_bug_vectors, bug_vector[i], code_vector[j], past_bugs)
    
    return similarity
    
def update_bug_tfidf(past_bugs, bug_data, storage_path):

    if len(past_bugs) == 0:
        start_time = time.time()
        print("get the document-level features for bugs...")
        idfs = get_docu_feature(bug_data, storage_path, True)
        print("the time consuming is %f s" %(time.time() - start_time))

        start_time = time.time()
        print("get the term-level features for bugs...")
        past_bug_vectors = tfidf_creation(bug_data, idfs, storage_path, True)
        print("the time consuming is %f s" %(time.time() - start_time))

        past_bugs = bug_data
        past_bugs = {k: v for k, v in sorted(past_bugs.items(), key = lambda date: date[1]["fixed_date"])}
        with open(os.path.join(storage_path + "bug_data.json"), "w") as f:
            json.dump(past_bugs, f)

        return past_bug_vectors, past_bugs

    else:
        added_bugs = []
        modified_bugs = []
        for bug_id, bug_cont in bug_data.items():
            bug_cont = bug_cont["content"]
            if not bug_id in past_bugs.keys():
                added_bugs.append([bug_id])
            elif not bug_cont == past_bugs[bug_id]:
                modified_bugs.append([bug_id])
        past_bug_vectors = update_tfidf_feature(bug_data, added_bugs, [], modified_bugs, storage_path)
        
        past_bugs.update(bug_data)
        past_bugs = {k: v for k, v in sorted(past_bugs.items(), key = lambda date: date[1]["fixed_date"])}
        with open(os.path.join(storage_path + "bug_data.json"), "w") as f:
            json.dump(past_bugs, f)

        return past_bug_vectors, past_bugs

def computing_bug_simi(tf_idfs, bug_vector, code_vector, past_bugs):
    
    count = 0
    bug_simi = 0
    for bug_id, bug_cont in past_bugs.items():
        
        if code_vector["id"][0].decode() in bug_cont["fixed_files"] and bug_cont["fixed_date"]<past_bugs[bug_vector["id"][0].decode()]["fixed_date"]:
            count += 1
            if not tf_idfs[tf_idfs["id"]==bug_id.encode()].size == 0:
                bug_simi += np.sum(tf_idfs[tf_idfs["id"]==bug_vector["id"][0]]["tf_idf"] * tf_idfs[tf_idfs["id"]==bug_id.encode()]["tf_idf"])/(np.linalg.norm(tf_idfs[tf_idfs["id"]==bug_vector["id"][0]]["tf_idf"]) * np.linalg.norm(tf_idfs[tf_idfs["id"]==bug_id.encode()]["tf_idf"]))
    if not count == 0:
        bug_simi /= count

    return bug_simi