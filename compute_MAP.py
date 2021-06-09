import os
import json
def get_map(path):
    ap10 = 0
    ap_all = 0
    with open(path) as f:
        ap_values = json.load(f)
        if len(ap_values):
            for ap in ap_values.values():
                ap10 += ap["AP@top10"]
                ap_all += ap["AP@all"]
            print("\t MAP@10", ap10/len(ap_values), "\t MAP@all", ap_all/len(ap_values))

get_map("./.incbl-data/cassandra/evaluation.json")