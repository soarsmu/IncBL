# Blinpy-app

**Blinpy** is a tool for locate bugs based on bug reports.

misc recordings to be sort out:

for text_processor.py, 

```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download en_core_web_sm
```

and if errors are reported in this step, try to install with source code.

```
pip install -U pip setuptools wheel
git clone https://github.com/explosion/spaCy
cd spaCy
export PYTHONPATH=`pwd`
pip install -r requirements.txt
python setup.py build_ext --inplace
pip install .
python -m spacy download en_core_web_sm
```
