# IncBL

**IncBL** is a tool for locate bugs based on bug reports.

## New design

1. 代码部分，尽可能降低耦合度，保持模块的独立性。只保持模块间的数据耦合，同时保持功能和过程的内聚。设计`incbl`一个class，其余模块作为function进行调用， 那么在执行时只需调用`incbl`类，然后顺序执行：`incbl.__init__()`，初始化时读取存储内容和输入的query，初次使用会完成index和idf的创建；`incbl.index_update()`，更新index，初次使用不执行；`incbl.idf_update()`，更新index，初次使用不执行；`incbl.localization()`，计算相似度并query返回结果，`incbl.evaluation()`，在有groundtruth的情况下计算MAP，MRR，ACC等；`incbl.fixed_bugs_update()`，在得到groundtruth的情况下更新fixed_bugs。线上使用时会通过一些utils function把repo的代码clone到本地进行计算，所以执行顺序相同，中间会插入一些API的通讯function来给用户反馈信息，见`server.py`；
2. 数据结构和存储部分，我的初始设计是，为了同时传递信息的标注和信息，在文件读取后都以dict形式进行传递，比如{bugid: bug information}，存储文件也是将dict存储为.npy文件方便读取；这一点有待商榷，我现在的新想法是通过数据库的表进行存储，因为：a. 我们需要clone代码到本地进行计算，同时会保存index.npy，idf.npy，gensim生成的tfidfmodel，fixed_bugs.npy，这样以文件形式存储会在运行时读取/改代好多文件，但是用数据库的话其实只用和代码有关的一张表就可以全部存储；b. 数据库也许通过设定Github API中的不可更改的值作为主键，解决唯一标识文件的问题。而且会方便未来的增量存储。这一点还没有在设计里体现，会之后加进去。
3. 关于使用的第三方库，改用Spacy来进行分词、去停用词和词还原，因为原来这个部分是手写的，用Spacy在大语料上会快不少；用Gensim来计算tf，idf，以及相应的model，因为a.它可以直接使用BugLocator claim有着最好效果的tf变种公式，并且可以快速单独输出tf矩阵；b.可以保存现有的tf-idf模型，我们对存下的模型手动的更新idf，方便计算。除此之外，如果未来的工作如果想要添加/改用新的embedding，Spacy和Gensim支持word2vec，doc2vec，bert等等很多representation的训练。

## Usage
### Test new features
run `bash env_config.sh`



# TODOs:

- [ ] Code file reader
	- [x] Source Code reader
	- [ ] Code parser
- [x] Bug reports reader
- [x] Text processor
	- [x] Tokenizer
	- [x] Stummer and Stopwords removal
- [ ] TF computing
	- [ ] TF matrix creation
	- [ ] TF matrix update
- [ ] IDF computing
	- [ ] IDF matrix creation
	- [ ] IDF matrix creation
- [ ] Similarity Computing
	- [ ] Bugs similarity
	- [ ] Code files and bugs similarity
	- [ ] Normalization
- [ ] GitHub integration
	- [ ] Clone and update repo
	- [ ] Get and reply issues
	- [ ] Reply PR comment
  
# Future Work

1. 如果文件删除，或者重新命名，或者修改路径，则和bug report无法构建关系，如何处理，或者缓解这个问题。
2. 是否意味着，需要存储更多的内容，是否可以进行增量存储；我们现在进行增量计算，只关心当前的矩阵，那么矩阵的历史是否需要保存。如果需要保存，肯定要进行增量存储。那么增量存储，用什么更合适？还是自己设计文件系统。
3. Branch，每个branch是否都要进行计算
4. bug report和code file之间的联系如何构建和维护。
5. information retrival的截断问题.....
6. 如何唯一标识一个文件。如果只是重命名，则MD5码。
7. Nerual IR的incremental


