# IncBL

**IncBL** is a tool for locate bugs based on bug reports.

## Usage
### Test new features
run `bash env_config.sh`



# TODOs:

1. 流程重构，比如normlaization的位置
2. 类重构
3. 存储结构重构 不要使用文件。
4. 设计的时候，要考虑future work

# Limitation

1. 如果文件删除，或者重新命名，或者修改路径，则和bug report无法构建关系，如何处理，或者缓解这个问题。
2. 是否意味着，需要存储更多的内容，是否可以进行增量存储；我们现在进行增量计算，只关心当前的矩阵，那么矩阵的历史是否需要保存。如果需要保存，肯定要进行增量存储。那么增量存储，用什么更合适？还是自己设计文件系统。
3. Branch，每个branch是否都要进行计算
4. bug report和code file之间的联系如何构建和维护。
5. information retrival的截断问题.....
6. 如何唯一标识一个文件。如果只是重命名，则MD5码。
7. Nerual IR的incremental


