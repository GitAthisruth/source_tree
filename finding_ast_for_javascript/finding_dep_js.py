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


def dep_search(file_to_check, files_inform,visited=None,tupled_dependencies=None):
    if visited is None:
        visited = set()
    dependencies = set()
    if tupled_dependencies is None:
        tupled_dependencies = []
    visited.add(file_to_check)
    for file_info in files_inform:
        file_to_check = file_to_check.replace(".js","")
        if file_to_check in file_info['imports']:
            dependencies.add(file_info['file_name'])  # Direct dependency
    result = [(file_to_check, item) for item in dependencies]#creating a list of tuple
    tupled_dependencies.extend(result)
    
    # Indirect dependency  
    for imp_file in list(dependencies):
        if imp_file not in visited:
            new_dependencies, new_tupled_dependencies = dep_search(imp_file, files_inform, visited, tupled_dependencies)
            dependencies.update(new_dependencies)#here we updating the dependencies only. 
    # print(f"tupled dependencies: {tupled_dependencies}")
    return list(dependencies),tupled_dependencies





def dependency_check(folder_path,file_to_check,file_inform): 
    all_file_path = []
    all_files = []
    for (dirpath,dirnames, filenames) in os.walk(folder_path):
                for file in filenames:
                    if file.endswith(".js"):
                        all_files.append(file)  
                        logging.info(f"all python files are appended to the list all_files.")
                        file_path = os.path.join(dirpath, file)
                        logging.info(f"file name :{file} file path {file_path}")
                        logging.info(f"get_imports function going to run")
                        logging.info(f"file path are going to append: {file_path}")
                        all_file_path.append(file_path)
    logging.info(f"file path appended successfully")
    logging.info(f"result is :{all_file_path}")
    with open(file_inform, "r") as file:
        file_name_imports = json.load(file)
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
    folder_path = path = "C:\\Users\\LENOVO\\Desktop\\JSAPP\\dep_for_java_script\\test"
    file_to_check = input(f"Give a valid file_name(.js): ")
    file_inform = "C:\\Users\\LENOVO\\Desktop\prizmora\\source_tree\\finding_ast_for_javascript\\import_file.json"
    file_info = dependency_check(folder_path,file_to_check,file_inform)
    print(file_info)