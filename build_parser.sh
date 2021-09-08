mkdir tree_sitter_src
cd tree_sitter_src

git clone https://github.com/tree-sitter/tree-sitter-java.git
git clone https://github.com/tree-sitter/tree-sitter-python.git

cd ..

python build_tree_sitter.py