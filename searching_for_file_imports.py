# task
"""Input:give a filename
Output: find the filenames that is import by the Input filename"""


#code for ."js" and ".py" files only

import os 
import json
import re
from glob import glob

import pandas as pd

import main


# folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 

def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import", "from"))]
            # print(f"content is : {content_y}")
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
                regex = r"(?:import\s+([\w\.]+)|from\s+([\w\.]+)\s+import)"
                matches = re.findall(regex,val)
                for match in matches:
                    module_name = match[0] or match[1]
                    if "." in module_name:
                        module_name = module_name.split(".")[-1]
                        imports.append(module_name)
                    else:
                        imports.append(module_name)
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



def dep_search(file_to_check, files_inform, folder_inform,seen=None):
    dependencies = set()
    seen = set()
    seen_rec = set()
    for file_info in files_inform:
        if file_to_check in file_info['imp'] and file_info['file_name'] not in seen:
            dependencies.add(file_info['file_name'])  # Direct dependency
    
    for imp_file in list(dependencies):
        if imp_file not in seen_rec:
            seen_rec.add(imp_file)
            dependencies.update(dep_search(imp_file,files_inform, seen))

    return list(dependencies)






def get_all_file_infos(folder_path, file_to_check):
    try:
        file_inform = []
        all_files = []
        imp_list = []
        folder_inform = []
        extensions = ('.py','.js','.java')

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
                        file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
        imp_list = dep_search(file_to_check,file_inform,folder_inform)

        
        with open('file_info_t.txt', 'w') as file:
            file.write(str(imp_list))
        
        with open("file_info_j.json", "w") as out_file:
            json.dump(str(imp_list), out_file, indent=6)
        
        return imp_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 
    file_to_check = input("Enter the file name(.js/.py) without the extension to check: ")
    
    file_info = get_all_file_infos(folder_path, file_to_check)
    print(file_info)

