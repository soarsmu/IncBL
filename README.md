# IncBL

**IncBL** is a tool for locate bugs based on bug reports.

## New design

Yesterday I finished code about manual computation functions by numpy to instead gensim lib. 

Now the data structure in our design is numpy.array, and we use words and paths for boolean indexing, namely, for querying a word's document frequency, we can df["word"], so is the tf.

The following implementation is as follows:

1. Multiprocessing support.

2. Data storage:

   For each user, a folder are created to store the word list, tf, df matrices. These data is stored as ".npy" file to fast read and update.
   The other information, namely code data and bug data, we store them in a database by MongoDB.
   For code data: each collection is `{"_id"(inherent):…, "repo_name":…, {"SHA":…, "file_path":…, "file_content":…}}`
   For bug data db: each collection is `{"_id"(inherent):…, "bug_id", "bug_content":…, "fixed_files":…}`
   When we get a new issue, do a git fetch to get all commits, then check the SHA and file_path to decide whether update the code file.
   Maybe this can be implemented by github API, I'm looking into it.

3. Update function



## TODOs:

- [x] Code file reader
	- [x] Source Code reader
	- [x] Code parser
- [x] Bug reports reader
- [x] Text processor
	- [x] Tokenizer
	- [x] Stummer and Stopwords removal
- [ ] TF computing
	- [ ] TF matrix creation
	- [ ] TF matrix update
- [ ] IDF computing
	- [ ] IDF matrix creation
	- [ ] IDF matrix update
- [ ] Similarity Computing
	- [ ] Bugs similarity
	- [ ] Code files and bugs similarity
	- [ ] Normalization
- [ ] Bug Localization
    - [ ] Ranking
    - [ ] Evaluation
- [ ] Data Storage (MongoDB)
    - [ ] Code files storage and update
    - [ ] Bug report storage and update
	- [ ] matrix storage and update
- [ ] GitHub Integration
	- [ ] Clone and update repo
	- [ ] Get and reply issues
	- [ ] Reply PR comment
  
## Future Work

1. 如果文件删除，或者重新命名，或者修改路径，则和bug report无法构建关系，如何处理，或者缓解这个问题。
2. 是否意味着，需要存储更多的内容，是否可以进行增量存储；我们现在进行增量计算，只关心当前的矩阵，那么矩阵的历史是否需要保存。如果需要保存，肯定要进行增量存储。那么增量存储，用什么更合适？还是自己设计文件系统。
3. Branch，每个branch是否都要进行计算
4. bug report和code file之间的联系如何构建和维护。
5. information retrival的截断问题.....
6. 如何唯一标识一个文件。如果只是重命名，则MD5码。
7. Nerual IR的incremental


