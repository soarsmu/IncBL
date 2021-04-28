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

To install Faiss:

```
git clone https://github.com/facebookresearch/faiss.git faiss_xx

cd faiss_xx

target_dir=$PWD/install_py

# often the system cmake is too old
cmake=path_to_compiled_cmake

$cmake -B build \
    -DFAISS_ENABLE_GPU=OFF \
    -DBLA_VENDOR=Intel10_64_dyn \
    -DMKL_LIBRARIES=$CONDA_PREFIX/lib \
    -DPython_EXECUTABLE=$(which python) \
    -DFAISS_OPT_LEVEL=avx2 \
    -DCMAKE_BUILD_TYPE=Release

make -C build -j 10

(cd build/faiss/python/ ; python setup.py install --prefix $target_dir )

(cd ..; PYTHONPATH=$target_dir/lib/python3.7/site-packages/faiss-1.6.3-py3.7.egg/ python  -c "
```
