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
# path = "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree\\visualising_ast\\file1.py"

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



def dep_search(all_file_path,file_to_check):
    direct_dependant = []
    indirect_dependant = []
    for file_path in all_file_path:
        file_name = os.path.basename(file_path)
        for import_values in get_imports(file_path):
            module = import_values.module
            name = import_values.name
            alias = import_values.alias
            logging.info(f"file : {file_name} get_import function successfully run and the result is: Module: {module}, Name: {name}, Alias: {alias}")
            #finding direct dependant files.
            if name[0] == file_to_check and file_name not in direct_dependant:
                logging.info(f"started to finding direct dependant files of the file to check and appending it to a list direct_dependent")
                direct_dependant.append(file_name)
                logging.info(f"file:{file_name} and module_name {name}")

        #searching for indirect dependency
        # logging.info(f"started to check for indirect dependency of file")

        # for file_name in direct_dependant:
        #     if file_path.endswith(file_name) and file_name not in indirect_dependant:
        #         logging.info(f"file paths for searching indirect dependant is added: file paths are {file_path}" )
        #         dependency_check               












folder_path = path = "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree"
file_to_check = input(f"Give a valid file_name: ")
# finding path to the files in a directory.
# 
def dependency_check(folder_path,file_to_check): 
    all_file_path = []
    dependent_file = []
    all_files = []
    for (dirpath,dirnames, filenames) in os.walk(folder_path):
                for file in filenames:
                    if file.endswith(".py"):
                        all_files.append(file)  
                        logging.info(f"all python files are appended to the list all_files.")
                        file_path = os.path.join(dirpath, file)
                        logging.info(f"file name :{file} file path {file_path}")
                        logging.info(f"get_imports function going to run")
                        logging.info(f"file path are going to append: {file_path}")
                        all_file_path.append(file_path)
                        logging.info(f"file path appended successfully")
                        logging.info(f"result is :{all_file_path}")

  
    #finding direct dependant files.
    logging.info(f"started to run dep_search function....")
    direct_dependent = dep_search(all_file_path,file_to_check)
    logging.info(f"direct dependant files are: {direct_dependent}")
    
    


    # print(direct_dependant)

    return dependent_file

print(dependency_check(folder_path,file_to_check))



