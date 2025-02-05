# task
"""Input:give a filename
Output: find the filenames that is import by the Input filename"""


#code for ."js" and ".py" files only

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
        with open(file_path, "r",encoding="utf8") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import", "from"))]
        return content_y
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None


import re

def extract_imports(content):
    try:
        imports = []
        for val in content:
            if ".js" not in val:
                regex = r"(?:import\s+([\w,\.]+)|from\s+([.\w]+)\s+import\s+([\w,*]+))"
                regex_relative = r"from\s+([.]+[\w]*)\s+import\s+([\w,*]+)"
                matches = re.findall(regex, val)
                for match in matches:
                    if match[0]: 
                        modules = [m.strip() for m in match[0].split(",")]
                        imports.extend(modules)
                    elif match[1]: 
                        imports.append(match[1])
                        if match[2]: 
                            functions = [f.strip() for f in match[2].split(",")]
                            imports.extend(functions)

                matches_relative = re.findall(regex_relative, val)
                if matches_relative:
                    for match in matches_relative:
                        modules = [m.strip() for m in match[1].split(",")]
                        imports.extend(modules)
            else:
                regex = r"(?:import\s+[^'\"]*['\"](?:.*/)?([\w]+)\.js['\"]|from\s+['\"](?:.*/)?([\w]+)\.js['\"])"
                matches = re.findall(regex,val)
                for match in matches:
                    module_name = match[0] or match[1]
                    imports.append(module_name)
        return list(set(imports))    
    except Exception as e:
        print(f"An error occured while extracting imports: {e}")
        return []



def dep_search(file_to_check, files_inform,visited=None,tupled_dependencies=None):
    if visited is None:
        visited = set()
    dependencies = set()
    if tupled_dependencies is None:
        tupled_dependencies = []
    visited.add(file_to_check)
    for file_info in files_inform:
        file_to_check = file_to_check.replace(".py","")
        if file_to_check in file_info['imp']:
            dependencies.add(file_info['file_name'])  # Direct dependency
    
    result = [(file_to_check, item) for item in dependencies]#creating a list of tuple
    tupled_dependencies.extend(result)
    
    # Indirect dependency  
    for imp_file in list(dependencies):
        if imp_file not in visited:
            new_dependencies, new_tupled_dependencies = dep_search(imp_file, files_inform, visited, tupled_dependencies)
            dependencies.update(new_dependencies)#here we updating the dependencies only. 

    return list(dependencies),tupled_dependencies




def get_all_file_infos(folder_path, file_to_check):
    try:
        file_inform = []
        all_files = []
        imp_list = []
        extensions = ('.py','.js',)

        if file_to_check.endswith(extensions):
            file_to_check = os.path.splitext(file_to_check)[0]#convert file without extension
        
        for ext in extensions: 
            all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
        for (dirpath,dirnames, filenames) in os.walk(folder_path):
            for file in filenames:
                if file.endswith(extensions):
                    file_path = os.path.join(dirpath, file)
                    file_contents = content_reader(file_path)
                    print(f"file_name:{file} and file_contents: {file_contents}")
                    if file_contents:
                        file_imports = extract_imports(file_contents)
                        file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
        result =  dep_search(file_to_check,file_inform)
        imp_list = result[0]
        tupled_dep = result[1]
        draw_tree(file_to_check,tupled_dep)
        imp_list_json = json.dumps({"file": file_to_check, "dependencies": imp_list}, indent=4)
        with open(f"{file_to_check}_dependencies.json", "w") as outfile:
            outfile.write(imp_list_json)
        with open(f'{file_to_check}_txt_file_info.txt', 'w') as file:
            file.write(imp_list_json)

        return imp_list_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


if __name__ == "__main__":
    folder_path = "C:\\Users\\LENOVO\\Desktop\\python_repo_to_check\\importlab"
    # folder_path =  "C:\\Users\\LENOVO\\Desktop\\python_/repo_to_check\\Qwen"
    # folder_path = "C:\\Users\\LENOVO\\Desktop\\flask_demo_project_case_management\\Frontend\\project-management"  
    # folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree"
    # folder_path = "C:\\Users\LENOVO\\Desktop\\python_repo_to_check\\Advanced-Artificial-Intelligence-Projects-with-Python" 
    file_to_check = input("Enter the file name(.js/.py) without the extension to check: ")
    # folder_path = os.path.normpath(folder_path)
    file_info = get_all_file_infos(folder_path, file_to_check)
    print(file_info)
