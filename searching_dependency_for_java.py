import networkx as nx
import matplotlib.pyplot as plt
import os 
import json
import re
from glob import glob

import pandas as pd



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



def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import","package"))]
        return content_y
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

def extract_imports(content):
    try:
        imports = []
        for val in content:
            regex = r"(?:import\s+([\w]+(?:\.[\w]+)*)(?:\.\*|;)?)|((package)\s+([\w]+(?:\.[\w]+)?)\s*;)"
            matches = re.findall(regex,val)
            for match in matches:
                module_name = match[0] or match[1]
                if "." in module_name:
                    module_name_ = module_name.split(".")[-1]
                    imports.append(module_name_)
                else:
                    imports.append(module_name)
        return list(set(imports))    
    except Exception as e:
        print(f"An error occured while extracting imports: {e}")
        return []
    


def dep_search(file_to_check, files_inform, folder_inform,visited=None,tupled_dependencies=None):
    dependencies = set()
    if visited is None:
        visited = set()
    parent_folder = None
    if tupled_dependencies is None:
        tupled_dependencies = []
    visited.add(file_to_check)
    for folder in folder_inform:
        if folder['folder_files'] == file_to_check:
            parent_folder = folder['folder_name']#if there is any folder name there.
            break 

    for file_info in files_inform:
        if file_to_check in file_info['imp']:
            dependencies.add(file_info['file_name'])  # Direct dependency
    
    if parent_folder:
        for file_info in files_inform:
            if parent_folder in file_info['imp']:
                dependencies.add(file_info['file_name'])  

    for imp_file in list(dependencies):
        if imp_file not in visited:
            new_dependencies, new_tupled_dependencies = dep_search(imp_file, files_inform,folder_inform,visited, tupled_dependencies)
            dependencies.update(new_dependencies)#here we updating the dependencies only. 
    result = [(file_to_check, item) for item in dependencies]#creating a list of tuple
    tupled_dependencies.extend(result)
    print(tupled_dependencies)
 
    
    return list(dependencies),tupled_dependencies



def dep_check_for_java(folder_path,file_to_check):
    file_to_check = "MyClass"
    file_inform = []
    folder_inform = []
    all_files = []
    imp_list = []
    extensions = ('.java')

    if file_to_check.endswith(extensions):
        file_to_check = os.path.splitext(file_to_check)[0]#convert file without extension
            
    for ext in extensions: 
        all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
    for (dirpath,dirnames, filenames) in os.walk(folder_path):
        for file in filenames:
            if file.endswith(extensions):
                file_path = os.path.join(dirpath, file)
                file_contents = content_reader(file_path)
                if file_contents:
                    file_imports = extract_imports(file_contents)
                    if "package" in file_imports[0]:
                        package_name = file_imports[0].replace("package ", "").replace(";", "").strip()
                        folder_inform.append({"folder_name":package_name,"folder_files":file.split(".")[0]})
                    else:    
                        file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
    result = dep_search(file_to_check,file_inform,folder_inform)
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
    file_to_check = input("Enter the file name(.java) without the extension to check: ")
    
    file_info = dep_check_for_java(folder_path, file_to_check)
    print(file_info)





           




