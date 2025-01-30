import ast
from collections import namedtuple
import os
import logging

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y--%m--%d %H:%M:%S",
        filename="python_ast.log"
    )


Import = namedtuple("Import", ["module", "name", "alias"])

# print(f"Named tuple of Import: {Import}")
path = "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree\\visualising_ast\\file1.py"

def get_imports(path):
    with open(path) as fh:        
       root = ast.parse(fh.read(), path)
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):  
            module = node.module.split('.')
        else:
            continue

        for n in node.names:
            yield Import(module, n.name.split('.'), n.asname)


# print(list(get_imports(path)))


folder_path = path = "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree"

# finding path to the files in a directory.
# 
def dependency_check(folder_path): 
    ls_files = []
    for (dirpath,dirnames, filenames) in os.walk(folder_path):
                for file in filenames:
                    if file.endswith(".py"):
                        # print(f"file {file}")
                        file_path = os.path.join(dirpath, file)
                        logging.info(f"file name :{file} file path {file_path}")
                        logging.info(f"get_imports function going to run")
                        logging.info(f"file path are going to append: {file_path}")
                        ls_files.append(file_path)
                        logging.info(f"file path appended successfully")
                        logging.info(f"result is :{ls_files}")

    #getting module names of a file.
    # print(ls_files)
    for file_path in ls_files:
        # print(file_path)
        file_name = os.path.basename(file_path)
        for import_values in get_imports(file_path):
            print(file_name,import_values)
            module = import_values.module
            name = import_values.name
            alias = import_values.alias
            logging.info(f"file : {file_name} get_import function successfully run and the result is: Module: {module}, Name: {name}, Alias: {alias}")
    return []

print(dependency_check(folder_path))



