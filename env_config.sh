# Here we creatre a virtual environment and install necessary libraries
conda create -n incbl python=3.7
conda activate incbl

# Install Spacy
pip install -U pip setuptools wheel
pip install -U spacy
{
    python -m spacy download en_core_web_sm     # This may cause error due to poor network
}||{
    conda install -c conda-forge spacy-model-en_core_web_sm
}

pip install --upgrade gensim
pip install tree_sitter
pip install python-dateutil