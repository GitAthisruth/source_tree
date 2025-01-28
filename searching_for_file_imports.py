# task
"""Input:give a filename
Output: find the filenames that is import by the Input filename"""


import os 
import json
import re
from glob import glob

import pandas as pd

import math_operation



folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 



def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import", "from"))]
            print(f"content is : {content_y}")
        return content_y
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read the file at {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file at {file_path}: {e}")
        return None


import re

def extract_imports(content):
    try:
        imports = []
        print(f"extracted contents: {content}")
        for val in content:
            if ".js" not in val:
                print(f"val in contents are: {val}")
                regex = r"(?:import\s+([\w\.]+)|from\s+([\w\.]+)\s+import)"
                matches = re.findall(regex,val)
                print(f"matches from content:{matches}")
                for match in matches:
                    module_name = match[0] or match[1]
                    if "." in module_name:
                        module_name = module_name.split(".")[-1]
                        imports.append(module_name)
                    else:
                        imports.append(module_name)
            else:
                regex = r"from\s+['\"](?:.*/)?([\w]+)\.js['\"]"
                matches = re.findall(regex,val)
                print("dhjjbhasdcjhbdsjhbds \n dsjhhjdsjhsjdhhjdsahgjchgjdhsjghjgdshjgcdhjgcdshjgcadshjgdcsahjg \n dshhjdshjdsahjdshjdsajhadshjdsahjg \n")
                print(f"matches from content:{matches}")
                for match in matches:
                    imports.append(match)
        return list(set(imports))    
    except Exception as e:
        print(f"An error occurred while extracting imports: {e}")
        return []



def dep_search(file_to_check,content_val,seen=None):
    if seen is None:
        seen = set()
    imp_set = set()
    for i in content_val:
        if file_to_check in i["imp"] and i["file_name"] not in seen:
            imp_set.add(i["file_name"])
            seen.add(i["file_name"])
    for imp_file in list(imp_set):
        imp_set.update(dep_search(imp_file, content_val, seen))

    return list(imp_set)
    






def get_all_file_infos(folder_path, file_to_check):
    try:
        file_inform = []
        all_files = []
        imp_list = []
        extensions = ('.py','.js')

        if file_to_check.endswith(extensions):
            file_to_check = os.path.splitext(file_to_check)[0]
        
        for ext in extensions: 
            print(f"ext is: {ext}")
            all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
        print(f"all_files {all_files}")
        for (dirpath,dirnames, filenames) in os.walk(folder_path):
            for file in filenames:
                if file.endswith(extensions):
                    # print(f"file {file}")
                    file_path = os.path.join(dirpath, file)
                    file_contents = content_reader(file_path)
                    # print(f"file:{file} file_contents: {file_contents}") # import as list of values
                    
                    if file_contents:
                        file_imports = extract_imports(file_contents)
                        print(f"file {file} and file_imports {file_imports}")
                        file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
        # print(f"file_inform {file_inform}")
        imp_list = dep_search(file_to_check,file_inform)

        
        with open('file_info_t.txt', 'w') as file:
            file.write(str(imp_list))
        
        # Save the results to a JSON file
        with open("file_info_j.json", "w") as out_file:
            json.dump(str(imp_list), out_file, indent=6)
        
        return imp_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    # folder_path = input("Enter the folder path: ")
    folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 
    file_to_check = input("Enter the file name to check: ")
    
    file_info = get_all_file_infos(folder_path, file_to_check)
    print(file_info)

