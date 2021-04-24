from xml.dom.minidom import parse
from text_processor import split_nature_langugage
from utils.bl_text_processor import stem
from utils.bl_text_processor import is_stopword
import os
from utils.bug import Bug
from sklearn.feature_extraction.text import TfidfVectorizer
import math
import json
from multiprocessing import Pool, Process, Queue, Manager
import multiprocessing
import time
import numpy as np
import re

manager = multiprocessing.Manager()

q = manager.Queue()
q_to_store = manager.Queue()


class bug_corpus_creator():
    '''
    This class parse bug reports and generate some bug information.
    '''

    

    def __init__(self, path_to_store):
        self.path_to_store = path_to_store
        # self.
        if not os.path.exists(self.path_to_store):
            os.makedirs(self.path_to_store)

    def xml_parser(self, path):
        '''
        It can parse bug report with format of both Bugzbook, bugLocator paper, Denchmark_BRs projects
        '''
        class_name = []
        with open(os.path.join(self.path_to_store, 'ClassName.txt')) as f:
            for line in f.readlines():
                class_name.append(line.split('\t')[1].strip())
        
        allBugData = {} # 用于存储bug数据，包括repo名称，bugReport信息
        allBugData['bugReportData'] = {}

        DOMTree = parse(path) # 读取存储bug report的XML文件
        bugreports = DOMTree.documentElement
        bugrepositoryName = bugreports.getAttribute('name')
        allBugData['repositoryName'] = bugrepositoryName
        bugReportList = bugreports.getElementsByTagName("bug")
        commitDataList = bugreports.getElementsByTagName("commit")
        
        if len(commitDataList) == 0:
            for bugReport in bugReportList:
                bugdata = {}

                bugdata['id'] = bugReport.getAttribute("id")
                # However, BugLocator only allows id as Integer
                bugdata['opendate'] = bugReport.getAttribute("opendate")
                bugdata['fixdate'] = bugReport.getAttribute("fixdate")
                summary = bugReport.getElementsByTagName("summary")
                try:
                    summaryText = summary[0].childNodes[0].data # 得到summary信息
                except:
                    summary = bugReport.getElementsByTagName("title")
                    summaryText = summary[0].childNodes[0].data # 得到summary信息
                # Bugzbook中不是用summary，而是title
                if len(summary[0].childNodes) > 0:
                    summaryText = summary[0].childNodes[0].data # 得到summary信息
                else:
                    summaryText = ''
                bugdata['summary'] = summaryText
                
                description = bugReport.getElementsByTagName("description")
                # 发现description有可能是空的，因此做此处理
                if len(description[0].childNodes) > 0:
                    descriptionText = description[0].childNodes[0].data # 得到description信息
                else:
                    descriptionText = ''
                bugdata['description'] = descriptionText

                fixedFiles = bugReport.getElementsByTagName("file")
                bugdata['files'] = []
                is_wrong_with_fixed_files = False
                for file in fixedFiles:
                    try:
                        fileName = file.childNodes[0].data
                    except:
                        fileName = ""
                        is_wrong_with_fixed_files = True
                    if not fileName in class_name:
                        is_wrong_with_fixed_files = True
                    bugdata['files'].append(fileName)
                if is_wrong_with_fixed_files:
                    continue
                allBugData['bugReportData'][bugReport.getAttribute("id")] = bugdata
        else:
            for bugReport, commitData in zip(bugReportList, commitDataList):
                bugdata = {}

                bugdata['id'] = bugReport.getAttribute("id")
                bugdata['opendate'] = bugReport.getAttribute("open_date")
                bugdata['fixdate'] = bugReport.getAttribute("closed_time")
                summary = bugReport.getElementsByTagName("summary")
                summaryText = summary[0].childNodes[0].data # 得到summary信息
                bugdata['summary'] = summaryText
                
                description = bugReport.getElementsByTagName("description")
                # 发现description有可能是空的，因此做此处理
                if len(description[0].childNodes) > 0:
                    descriptionText = description[0].childNodes[0].data # 得到description信息
                else:
                    descriptionText = ''
                bugdata['description'] = descriptionText
                # modification = commitData.getElementsByTagName("modification")
                #fixedFiles = modification[0].getAttribute("new_name")
                fixedFiles = commitData.getElementsByTagName("modification")
                bugdata['files'] = []
                for index, file in enumerate(fixedFiles):
                    try:
                        fileName = file.getAttribute("new_name").replace('\\', '/')
                    except:
                        fileName = ""
                    bugdata['files'].append(fileName)
                # if is_wrong_with_fixed_files:
                #     continue
                allBugData['bugReportData'][bugReport.getAttribute("id")] = bugdata
        # print(allBugData['bugReportData'])
        return allBugData

    def json_parser(self, path):
        '''
        It can parse bug report with format of BUGL projects
        '''
        class_name = []
        with open(os.path.join(self.path_to_store, 'ClassName.txt')) as f:
            for line in f.readlines():
                class_name.append(line.split('\t')[1].strip())
        
        allBugData = {} # 用于存储bug数据，包括repo名称，bugReport信息
        allBugData['bugReportData'] = {}
        

        with open(path) as bugReportList: # 读取存储bug report的JSON文件
            line = bugReportList.readline()
            bugReports = json.loads(line)

            for index in bugReports['closed_issues']:
                bugData = {}
                if not len(bugReports['closed_issues'][index]['files_changed']) == 0:
                    bugData['id'] = bugReports['closed_issues'][index]['issue_id'].replace("#", "")
                    bugData['summary'] = bugReports['closed_issues'][index]['issue_summary']
                    bugData['description'] = bugReports['closed_issues'][index]['issue_description']
                    bugData['opendate'] = bugReports['closed_issues'][index]['issue_reporting_time']
                    bugData['fixdate'] = bugReports['closed_issues'][index]['issue_fixed_time']
                    fileNames = bugReports['closed_issues'][index]['files_changed']
                    bugData['files'] = []
                    for fileName in fileNames:
                        bugData['files'].append("/" + fileName[1])
                    allBugData['bugReportData'][bugData['id']] = bugData
            
        return allBugData

    def create_bug_list(self, allBugData):
        self.buglist = []
        for i, bug_info in enumerate(allBugData['bugReportData'].values()):
            bug = Bug(bug_info['id'], 
                    bug_info['opendate'], 
                    bug_info['fixdate'], 
                    bug_info['summary'],
                    bug_info['description'],
                    bug_info['files'])
            self.buglist.append(bug)

    def write_corpus(self, bug):
        '''
        接受bug的信息，以及存储corpus的路径
        '''
        dir_to_store = os.path.join(self.path_to_store, 'BugCorpus')
        # 提取bug的信息，summary和description
        content = bug.bug_summary + ' ' + bug.bug_description
        # 分词 参照Splitter.splitNatureLangugage()
        splited_words = split_nature_langugage(content)

        # To-Do: 创建corpus
        corpus = []
        for single_word in splited_words:
            # To-Do: Stem
            word = stem(single_word.lower())
            # To-Do: 去除Stopwords
            if not is_stopword(word):
                corpus.append(word)

        # To-Do: 写入corpus
        if not os.path.exists(dir_to_store):
            os.makedirs(dir_to_store)
        with open(os.path.join(dir_to_store, bug.bugid + '.txt'), 'w') as f:
            f.write(' '.join(corpus))


        return corpus

    def create_sortedId(self):
        with open(os.path.join(self.path_to_store, 'SortedId.txt'), 'w') as f:
            for single_bug in self.buglist:
                f.write(single_bug.bugid + '\t' + single_bug.fix_date + '\n')

    def create_fixLink(self):
        with open(os.path.join(self.path_to_store, 'FixLink.txt'), 'w') as f:
            for single_bug in self.buglist:
                for single_ground_truth in single_bug.ground_truth:
                    f.write(single_bug.bugid + '\t' + single_ground_truth + '\n')

    def create_bug_vector(self, path_to_bugCorpus):
        tv = TfidfVectorizer(use_idf=True, smooth_idf=False, norm=None)
        document = []

        bug_corpus_sequence = []
        for corpus in os.listdir(path_to_bugCorpus):
            with open(os.path.join(path_to_bugCorpus, corpus)) as f:
                document.append(re.sub(r'\w*\d\w*', '', f.read()).strip())
                bug_corpus_sequence.append(corpus)

        tfidf_model = TfidfVectorizer().fit(document)
        sparse_result = tfidf_model.transform(document) 
        with open(os.path.join(self.path_to_store, 'BugTermList.txt'), 'w') as f:
            for term in tfidf_model.get_feature_names():
                f.write(term + '\n')
        with open(os.path.join(self.path_to_store, 'BugVector.txt'), 'w') as f:
            for position, i in enumerate(sparse_result.todense()):
                f.write(bug_corpus_sequence[position] + '; ')
                for index, value in enumerate(i.tolist()[0]):
                    if value <= 0:
                        continue
                    f.write(str(index) + ':' + str(value) + ' ')
                f.write('\n')



    def compute_similarity(self):
        '''
        计算bug report的similarity
        尽量使用参数传递的方式，方便进行单元测试
        '''
        # To-Do: 得到wordCount
        with open(os.path.join(self.path_to_store, 'BugTermList.txt')) as f:
            wordCount = len(f.readlines())

        # To-Do: 读取SortedId，得到所有的BugID写入一个list
        bug_id_list = []
        with open(os.path.join(self.path_to_store, "SortedId.txt")) as f:
            for line in f.readlines():
                bug_id = line.split('\t')[0]
                bug_id_list.append(bug_id)

        # To-Do: 读取bugVector并存到一个dictionary中
        bug_vector_dict = {}
        with open(os.path.join(self.path_to_store, "BugVector.txt")) as f: 
            for bug_vector_data in f.readlines():
                bug_id = bug_vector_data.split('.')[0]
                vector_info = bug_vector_data.split(';')[1]
                # 现在处理vector_info，将其转化为一个list
                bug_vector = [0] * wordCount
                for single_value in vector_info.strip().split(' '):
                    position = single_value.split(':')[0]
                    value = single_value.split(":")[1]
                    bug_vector[int(position)] = float(value)
                    # 值转化为整数和浮点数 存入一个
                bug_vector_dict[bug_id] = bug_vector

        # To-Do: 计算Similarity CosineValue
        print('Start to compute similarity in bug corpus')
        content_to_write = []
        
        for i, first_bug_id in enumerate(bug_id_list):
            q.put([i, first_bug_id])
            continue

        numList = []
        for i in range(8) :
            p = multiprocessing.Process(target=self.compute_simi, args=(bug_vector_dict, wordCount, bug_id_list))
            numList.append(p)
            p.start()

        for i in numList:
            i.join()


        # 写入Similarity
        path_to_similarity = os.path.join(self.path_to_store, "BugSimilarity.txt")
        with open(path_to_similarity, 'w') as f:
            while not q_to_store.empty():
                output = q_to_store.get()
                f.write(output + '\n')

        return path_to_similarity

    def compute_simi(self, bug_vector_dict, wordCount, bug_id_list):
        '''for multi processing usage'''
        while True:
            if not q.empty():
                index, first_bug_id = q.get()

                first_bug_vector = bug_vector_dict[first_bug_id]
                output = str(first_bug_id) + ';'
                for j in range(index):
                    second_bug_id = bug_id_list[j]
                    second_bug_vector = bug_vector_dict[second_bug_id]
                    # 计算similarity
                    len1 = 0.0
                    len2 = 0.0
                    product = 0.0
                    for i in range(wordCount):
                        len1 += first_bug_vector[i] * first_bug_vector[i]
                        len2 += second_bug_vector[i] * second_bug_vector[i]
                        product += first_bug_vector[i] * second_bug_vector[i]
                    similarity = product / (math.sqrt(len1) * math.sqrt(len2))
                    output = output + second_bug_id + ':' + str(similarity) + ' '
                
                q_to_store.put(output)

            else:
                return
