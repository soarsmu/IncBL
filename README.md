[![Install App](https://img.shields.io/badge/GitHub%20App-Install-blueviolet?logo=github)](https://github.com/apps/incbl)

## What is IncBL?

IncBL (**Inc**remental **B**ug **L**ocalization) is an efficient information retrieval-based bug localization tool for evolving software repositories. It can store and update model parameters incrementally to save running time without sacrificing accuracy. IncBL is implemented as an open-source GitHub app that can analyze the issues labelled as **bug** and comment with the suspicious code files to remind developers.

## How to use IncBL app?

When using IncBL, all you need to do is adding IncBL to your GitHub repositories by following this [link](https://github.com/apps/incbl). Once IncBL being installed, it will automatically analyze the codebases and past bug reports. Each time when a new issue tagged with **bug** is raised, IncBL updates models incrementally and locates relevant buggy files for this report. After files are retrieved, IncBL posts the top 10 most relevant files in the issue so developers can get notified.

A video demonstration of IncBL can found [here]().

## How to customize and run IncBL locally?

First, fork this repository and run `bash env_config.sh` to create a virtual environment and install necessary dependencies. Then, run `python local.py -h` to find the usage instructions.

There are three positional arguments in IncBL:

- `incbl_root`: IncBL's root directory
- `bug_report_directory`: Bug report directory
- `code_base_path`: Codebase directory

There are two optional argument you may care about when localizing bugs in multi-language project:

`-ft [file_type_list]`
The `file_type_list` is to clarify the suffixes of files to be processed, in other words, they represents the programming languages. You can specify like `-ft ["java", "py"]`.
`-sp storage_path`
This is for storage of incremental data.

One usage example is: `python local.py ./IncBL ./data/example.XML /dataset/example -ft ["java", "py"] -sp ./data` It means that:

- The bug report is `./data/example.XML`
- The codebase is `/dataset/example`
- IncBL will localize bug in `java` and `python` files, and save incremental data in `./data` folder.

The localizing results and the Mean Average Presion (if ground truths exist) will be returned at the terminal.

## Who develops IncBL?

IncBL is developed by [Zhou YANG](https://yangzhou6666.github.io/), [Jieke SHI](http://jiekeshi.github.io/), [David LO](http://www.mysmu.edu/faculty/davidlo/) and [Shaowei WANG](https://sites.google.com/site/wswshaoweiwang) from the Singapore Management University and University of Manitoba.
