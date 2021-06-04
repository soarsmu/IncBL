# IncBL

**IncBL** is a tool for locate bugs based on bug reports.

## TODOs:

- [x] Code file reader
	- [x] Source Code reader
	- [x] Code parser
- [x] Bug reports reader
- [x] Text processor
	- [x] Tokenizer
	- [x] Stummer and Stopwords removal
- [x] TF computing
	- [x] TF matrix creation
	- [x] TF matrix update
- [x] IDF computing
	- [x] IDF matrix creation
	- [x] IDF matrix update
- [x] Similarity Computing
	- [x] Bugs similarity
	- [x] Code files and bugs similarity
	- [x] Normalization
- [x] Bug Localization
    - [x] Ranking
    - [x] Evaluation
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


