[![Install App](https://img.shields.io/badge/GitHub%20App-Install-blueviolet?logo=github)](https://github.com/apps/incbl)

## What is IncBL?

IncBL (**Inc**remental **B**ug **L**ocalization) is an efficient information retrieval-based bug localization tool that can store and update model incrementally to save running time. IncBL is implemented as an open-source GitHub app that can analyze the issues labelled as **bug** and comment with the suspicious code files to remind developers.

## What are IncBL's features?

IncBL focuses on improving the efficiency by combining two main features:

- IncBL refactors BugLocator with multiple-processing feature. It also utilizes bug history information and file length normalization to enhance accuracy, but can run 20 times faster than original BugLocator.
- IncBL can store the Incremental update.

IncBL can be installed as an GitHub app in any GitHub repository. IncBL can also be locally-deployed as a docker tool.

A video demonstration of IncBL can found [here]().

## Why we need IncBL?

IncBL aims to help users provide better bug reports, increase the productivity of developers, and help researchers in their investigations.

## How to use IncBL app?

When use IncBL, all you need to do is adding IncBL to your GitHub repositories by following this [link](https://github.com/apps/incbl). Once installed, IncBL will analyze any incoming issue within your repositories and return the names of buggy files for **bug** issues.

## How to customize and run IncBL locally?

First, fork the repository and run：

## Who develops IncBL?

IncBL is developed by [Zhou YANG](https://yangzhou6666.github.io/), [Jieke SHI](http://jiekeshi.github.io/), [David LO](http://www.mysmu.edu/faculty/davidlo/) and [Shaowei WANG](https://sites.google.com/site/wswshaoweiwang) from the Singapore Management University and University of Manitoba.
