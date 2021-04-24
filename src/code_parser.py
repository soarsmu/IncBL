from tree_sitter import Language, Parser

# These code can be used when adding new language support

# Language.build_library(
#     # Store the library in the `build` directory
#     './build/my-languages.so',

#     # Include one or more languages, need to clone the existing language repos from https://github.com/tree-sitter
#     [
#         '/home/jack/tree-sitter-bash',
#         '/home/jack/tree-sitter-python',
#         '/home/jack/tree-sitter-java',
#         '/home/jack/tree-sitter-c'

#     ]
# )

BASH_LANGUAGE = Language('./build/my-languages.so', 'bash')
PY_LANGUAGE = Language('./build/my-languages.so', 'python')
JAVA_LANGUAGE = Language('./build/my-languages.so', 'java')
C_LANGUAGE = Language('./build/my-languages.so', 'c')

parser_java = Parser()
parser_java.set_language(JAVA_LANGUAGE)

parser_py = Parser()
parser_py.set_language(PY_LANGUAGE)