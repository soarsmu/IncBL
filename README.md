[![Install App](https://img.shields.io/badge/GitHub%20App-Install-blueviolet?logo=github)](https://github.com/apps/incbl)

## What is IncBL?

[IncBL (**Inc**remental **B**ug **L**ocalization)](https://arxiv.org/abs/2106.07413) is an efficient information retrieval-based bug localization tool for evolving software repositories. It can store and update model parameters incrementally to save running time without sacrificing accuracy. IncBL is implemented as an open-source GitHub app that can analyze the issues labelled as **bug** and comment with the suspicious code files to remind developers.

## How to use IncBL app?

When using IncBL, all you need to do is installing IncBL to your GitHub repositories by following this [link](https://github.com/apps/incbl). Once IncBL being installed, it will automatically analyze the codebases and past bug reports. Each time when a new issue tagged with **bug** is raised, IncBL updates models incrementally and localizes relevant buggy files for this issue. After files are retrieved, IncBL posts the top 10 most relevant files in the issue so developers can get notified.

A video demonstration of IncBL can found [here](https://youtu.be/G4gMuvlJSb0).

## How to customize and run IncBL locally?

First, fork this repository and run `bash env_config.sh` to create a virtual environment and install necessary dependencies. Then, run `python local.py -h` to find the usage instructions.

There are three positional arguments in IncBL:

- `incbl_root`: IncBL's root directory
- `bug_report_directory`: Bug report directory
- `code_base_path`: Codebase directory

There are two optional argument you may care about when localizing bugs in multi-language project:

- `-ft [file_type_list]` The `file_type_list` is to clarify the suffixes of files to be processed, in other words, they represents the programming languages. You can specify like `-ft ["java", "py"]`.

- `-sp storage_path` This is for storage of incremental data.

One usage example is: `python local.py ./IncBL ./data/example.XML /dataset/example -ft ["java", "py"] -sp ./data` It means that:

- The bug report is `./data/example.XML`
- The codebase is `/dataset/example`
- IncBL will localize bug in `java` and `python` files, and save incremental data in `./data` folder.

The localizing results and the Mean Average Precision (if ground truths exist) will be returned to the terminal.

## Evaluation Results

We evaluate IncBL on [Bugzbook](https://engineering.purdue.edu/RVL/Bugzbook/) dataset. On the Bugzbook dataset, IncBL can significantly reduce the running time for locating bugs in continuously evolving repositories by **77.79%** (i.e., **4.5 times faster**) on average compared with the original BugLocator. IncBL can also achieve a Mean Average Precision (MAP) of **0.331** – on average, the correct files appear in the **top 3 locations**. The dataset and detailed experimental results can be downloaded from this [link](https://smu-my.sharepoint.com/:f:/g/personal/jiekeshi_smu_edu_sg/EnjVSGkHWHJEkgNpEY570VcBagyJf2aBdGnU5yI4MyiqTw?e=BCpRO7). For the downloaded files:
```
IncBL_data
    - datasets
        - Bugzbook_reports ----------- The original full dataset from Bugzbook.
        - cleaning_Bugzbook ---------- The clean dataset by removing non-code files in ground-truths.
        - RQ1_dataset -----------------The sampled 381 reports considering a 95% confidence level and 5% interval to measure running time.
    - results
        - RQ1_results ------------------- Running time of IncBL and BugLocator on RQ1_dataset
        - RQ2_results ------------------- Average Precision of IncBL on Bugzbook
```

## Who develops IncBL?

IncBL is developed by [Zhou YANG](https://yangzhou6666.github.io/), [Jieke SHI](http://jiekeshi.github.io/), [David LO](http://www.mysmu.edu/faculty/davidlo/) and [Shaowei WANG](https://sites.google.com/site/wswshaoweiwang) from the Singapore Management University and University of Manitoba.

If you meet any problems when using the tool, please contact Jieke SHI by [jiekeshi@smu.edu.sg](mailto:jiekeshi@smu.edu.sg). Many thanks!

```
@misc{yang2021incbl,
      title={IncBL: Incremental Bug Localization}, 
      author={Zhou Yang and Jieke Shi and Shaowei Wang and David Lo},
      year={2021},
      eprint={2106.07413},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```