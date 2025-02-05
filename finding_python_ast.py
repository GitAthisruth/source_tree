import ast
import os
import logging
import networkx as nx
import matplotlib.pyplot as plt
import json

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y--%m--%d %H:%M:%S",
        filename="python_ast.log"
    )


def draw_tree(file_to_check,tupled_dependency):
    G = nx.DiGraph()
    G.add_node(file_to_check)
    G.add_edges_from(tupled_dependency)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G,k=1,seed=3)
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='violet', font_size=6, font_weight=None, arrows=True,width=0.3)
    plt.title("File Dependency Tree Structure")
    plt.savefig(f"{file_to_check}py_file_tree", format="png")
    plt.show()







def get_imports(all_file_path):
    print(f"all file paths: {all_file_path}")
    file_name_imports = []
    for file_path in all_file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), file_path)
        file_name_= os.path.basename(file_path)
        file_name_ = file_name_.replace(".py","")
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # imports.append(("import", alias.name, alias.asname))#import pandas as pd
                    file_name_imports.append({"file_name":file_name_,"imports":[alias.name]})
            elif isinstance(node, ast.ImportFrom):#from numpy import array as arr
                for alias in node.names:
                    # imports.append(("from", node.module, alias.name, alias.asname))
                    file_name_imports.append({"file_name":file_name_,"imports":[node.module,alias.name]})
    return file_name_imports






def dep_search(file_to_check, files_inform,visited=None,tupled_dependencies=None):
    if visited is None:
        visited = set()
    dependencies = set()
    if tupled_dependencies is None:
        tupled_dependencies = []
    visited.add(file_to_check)
    for file_info in files_inform:
        file_to_check = file_to_check.replace(".py","")
        if file_to_check in file_info['imports']:
            dependencies.add(file_info['file_name'])  # Direct dependency
    result = [(file_to_check, item) for item in dependencies]#creating a list of tuple
    tupled_dependencies.extend(result)
    
    # Indirect dependency  
    for imp_file in list(dependencies):
        if imp_file not in visited:
            new_dependencies, new_tupled_dependencies = dep_search(imp_file, files_inform, visited, tupled_dependencies)
            dependencies.update(new_dependencies)#here we updating the dependencies only. 

    return list(dependencies),tupled_dependencies



 
def dependency_check(folder_path,file_to_check): 
    all_file_path = []
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
    file_name_imports = get_imports(all_file_path)
    print(f"file_name_imports:{file_name_imports}")
    result =  dep_search(file_to_check,file_name_imports)
    imp_list = result[0]
    tupled_dep = result[1]
    draw_tree(file_to_check,tupled_dep)
    imp_list_json = json.dumps({"file": file_to_check, "dependencies": imp_list}, indent=4)
    with open(f"{file_to_check}_dependencies.json", "w") as outfile:
        outfile.write(imp_list_json)
    with open(f'{file_to_check}_txt_file_info.txt', 'w') as file:
        file.write(imp_list_json)

    return imp_list_json



if __name__ == "__main__":
    folder_path =  "C:\\Users\\LENOVO\\Desktop\\javaProdemo"
    folder_path = path = "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree"
    file_to_check = input(f"Give a valid file_name(.py): ")
    file_info = dependency_check(folder_path,file_to_check)
    print(file_info)
