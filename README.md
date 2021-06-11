[![Install App](https://img.shields.io/badge/GitHub%20App-Install-blueviolet?logo=github)](https://github.com/apps/incbl)

## What is IncBL?

IncBL (**Inc**remental **B**ug **L**ocalization) is an efficient information retrieval-based bug localization tool for evolving software repositories. It can store and update model parameters incrementally to save running time without sacrificing accuracy. IncBL is implemented as an open-source GitHub app that can analyze the issues labelled as **bug** and comment with the suspicious code files to remind developers.

## What are IncBL's features?

IncBL focuses on improving the efficiency by combining two main features:

- IncBL refactors BugLocator with multiple-processing feature. It also utilizes bug history information and file length normalization to enhance accuracy, but can run 20 times faster than original BugLocator.
- IncBL can store the Incremental update.

IncBL can be installed as an GitHub app in any GitHub repository, and can also be deployed and run in local servers.

A video demonstration of IncBL can found [here]().

## How to use IncBL app?

When use IncBL, all you need to do is adding IncBL to your GitHub repositories by following this [link](https://github.com/apps/incbl). One IncBL being installed, it will automatically analyze the codebases and past bug reports. Each time when a new issue tagged with **bug** is raised, IncBL updates models incrementally and locates relevant buggy files for this report. After files are retrieved, IncBL posts the top 10 most relevant files in the issue so developers can get notified.

## How to customize and run IncBL locally?

First, fork this repository and run `bash env_config.sh` to create a virtual environment and install necessary dependencies.

python main.py -h to find the usage instructions.

There are three positional arguments:

bug_report_directory: Bug report directory
codebase: Codebase directory
store: Path to store results
There is one optional argument you may care about when localizing bugs in multi-language project:

-ft FILE_TYPE_LIST [FILE_TYPE_LIST ...]
There are the suffixes of files to be processed, in other words, they represents the programming languages. You can specify like -ft java py xml.

One usage example is: python main.py ./data/wicket.XML /media/zyang/dataset/wicket/ ./tmp -ft java xml It means that:

bug report is ./data/wicket.XML
codebase is /media/zyang/dataset/wicket/
I want to store the results in ./tmp
I want to localize bug in java and xml files.

The localizing results and the Mean Average Presion (if ground truths exist) will be returned at the terminal.

## Who develops IncBL?

IncBL is developed by [Zhou YANG](https://yangzhou6666.github.io/), [Jieke SHI](http://jiekeshi.github.io/), [David LO](http://www.mysmu.edu/faculty/davidlo/) and [Shaowei WANG](https://sites.google.com/site/wswshaoweiwang) from the Singapore Management University and University of Manitoba.
