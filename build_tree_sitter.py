from tree_sitter import Language, Parser
import os

Language.build_library(
    os.path.join('./', "lib/languages.so"),
    [
        './tree_sitter_src/tree-sitter-java',
        './tree_sitter_src/tree-sitter-python'
    ]
)