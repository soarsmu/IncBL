# Here we creatre a virtual environment and install necessary libraries
conda create -n multibl python=3.7
conda activate multibl
pip install pandas comment_parser python-magic tqdm matplotlib
pip install javalang xlrd eventlet timeout-decorator openpyxl prettytable sklearn pyclustering nltk
pip install tree_sitter # for parser