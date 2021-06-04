import json
import os
import numpy as np

def compute_similarity(bug_vector, code_vector, bug_data, past_bugs, storage_path):

    similarity = np.zeros((bug_vector.shape[0], code_vector.shape[0]), dtype=[("bug", "a30"),("file", "a250"), ("score", "f4")])

    for i in range(bug_vector.shape[0]):
        similarity[i]["bug"] = bug_vector[i]["id"][0]

        if not os.path.exists(os.path.join(storage_path, "past_bugs_tfidf.npy")):
            for j in range(code_vector.shape[0]):
                similarity[i][j]["file"] = code_vector[j]["id"][0]
                similarity[i][j]["score"] = (0.5 + 0.5 * np.sum(bug_vector[i]["tf_idf"] * code_vector[j]["tf_idf"])/(np.linalg.norm(bug_vector[i]["tf_idf"]) * np.linalg.norm(code_vector[j]["tf_idf"]))) * code_vector[j]["norm"][0]
            
            past_bugs_tfidf = np.asarray([bug_vector[i]])
            np.save(os.path.join(storage_path, "past_bugs_tfidf.npy"), past_bugs_tfidf)
            
        else:
            past_bugs_tfidf = update_past_tfidf(bug_vector[i], past_bugs, storage_path)
            for j in range(code_vector.shape[0]):
                alpha = 0.2
                similarity[i][j]["file"] = code_vector[j]["id"][0]
                similarity[i][j]["score"] = (1 - alpha) * (0.5 + 0.5 * np.sum(bug_vector[i]["tf_idf"] * code_vector[j]["tf_idf"])/(np.linalg.norm(bug_vector[i]["tf_idf"]) * np.linalg.norm(code_vector[j]["tf_idf"]))) * code_vector[j]["norm"][0] + alpha * computing_bug_simi(past_bugs_tfidf, bug_vector[i], code_vector[j], past_bugs)
        
        past_bugs.update({bug_vector[i]["id"][0].decode(): bug_data[bug_vector[i]["id"][0].decode()]})
    with open(os.path.join(storage_path + "bug_data.json"), "w") as f:
        json.dump(past_bugs, f)
    return similarity 

def update_past_tfidf(bug_vector, past_bugs, storage_path):

    tf_idfs = np.load(os.path.join(storage_path, "past_bugs_tfidf.npy"))
    if not bug_vector["id"][0] in tf_idfs["id"]:
        for term in bug_vector["term"]:
            if not term in tf_idfs["term"][0]:
                temp = np.zeros([tf_idf.shape[0], 1], dtype=[("id", "a250"),("term", "a30"), ("tf_idf", "f4"), ("norm", "f4")])
                temp["term"] = term
                tf_idfs = np.concatenate((tf_idfs, temp), 1)
        bug_vector = np.asarray([bug_vector])
        tf_idfs = np.concatenate((tf_idfs, bug_vector), 0)
        np.save(os.path.join(storage_path, "past_bugs_tfidf.npy"), tf_idfs)
    return tf_idfs

def computing_bug_simi(tf_idfs, bug_vector, code_vector, past_bugs):
    count = 0
    bug_simi = 0
    for bug_id, bug_cont in past_bugs.items():
        if code_vector["id"][0].decode() in bug_cont["fixed_files"]:
            count += 1
            if not tf_idfs[tf_idfs["id"]==bug_id.encode()].size == 0:
                bug_simi += np.sum(bug_vector["tf_idf"] * tf_idfs[tf_idfs["id"]==bug_id.encode()]["tf_idf"])/(np.linalg.norm(bug_vector["tf_idf"]) * np.linalg.norm(tf_idfs[tf_idfs["id"]==bug_id.encode()]["tf_idf"]))
    if not count == 0:
        bug_simi /= count
    return bug_simi