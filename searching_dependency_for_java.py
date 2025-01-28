import os 
import json
import re
from glob import glob

import pandas as pd

def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import"))]
            # print(f"content is : {content_y}")
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


def dep_search(file_to_check,content_val,file_and_package,seen=None):
    if seen is None:
        seen = set()
    imp_set = set()
    print(f"type:{type(file_and_package)}")
    print(f"file and package: {file_and_package}")
    print(f"content val: {content_val}")
    for i in content_val:
        print(f"content_i in deep_search: {i}")
        if file_to_check in i["imp"] and i["file_name"] not in seen:
            print(f"imp of {i['imp']}")
            imp_set.add(i["file_name"])
            seen.add(i["file_name"])
        elif file_and_package and isinstance(file_and_package,dict) == True and file_to_check in i["imp"]:
            for file_key in file_and_package:
                print(f"file_key: {file_key}")
                if file_to_check in file_and_package[file_key]:
                    imp_set.update(file_and_package[file_key])


    for imp_file in list(imp_set):
        print("dhjdjdjkjkdhjdhjdj")
        imp_set.update(dep_search(imp_file, content_val, seen))
    return list(imp_set)



def extract_imports(content):
    try:
        imports = []
        # print(f"extracted contents: {content}")
        for val in content:
            # print(f"val in contents are: {val}")
            regex = r"import\s+([\w]+(?:\.[\w]+)*)(?:\.\*|;)?"
            matches = re.findall(regex,val)
            # print(f"matches from content:{matches}")
            for match in matches:
                # print(f"match: {match}")
                if "." in match:
                    # print(f"match: {match}")
                    module_name = match.split(".")[-1]
                    imports.append(module_name)
                else:
                    # print(f"else: match {match}")
                    imports.append(match)
        return list(set(imports))    
    except Exception as e:
        # print(f"An error occured while extracting imports: {e}")
        return []
    
folder_path =  "C:\\Users\\LENOVO\\Desktop\\javaProdemo"

file_to_check = "App"

file_inform = []
all_files = []
imp_list = []
file_and_package_names= {}
extensions = ('.py','.js','.java')

if file_to_check.endswith(extensions):
    file_to_check = os.path.splitext(file_to_check)[0]
    # print(f"file_to_check:{file_to_check}")
        
for ext in extensions: 
    # print(f"ext is: {ext}")
    all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
    # print(f"all_files {all_files}")
for (dirpath,dirnames, filenames) in os.walk(folder_path):
    # print(f"dirpath:{dirpath} dirname:{dirnames} filename:{filenames}")#here we can check for the dir name if that is imported to any java files.then all the class are dependent to that file.
    for file in filenames:
        if file.endswith(extensions):
            # print(f"file {file}")
            file_path = os.path.join(dirpath, file)
            folder_name = os.path.split(dirpath)[-1]
            file_name = os.path.basename(file_path).split(".")[0]
            # print(f"dirpath: {os.path.split(dirpath)[-1]}")
            # print(f"file_path_:{file_path}")
            # print(f"folder_name:{folder_name} and file_name: {file_name}")
            # print(f"file_and_packages: {file_and_package_names}")
            if folder_name in file_and_package_names:
                file_and_package_names[folder_name].append(file_name)
            else:
                file_and_package_names[folder_name] = [file_name]
            # print(f"file_and_packages: {file_and_package_names}")
            file_contents = content_reader(file_path)
            # print(f"file:{file} file_contents: {file_contents}") 
            if file_contents:
                file_imports = extract_imports(file_contents)
                # print(f"file {file} and file_imports {file_imports}")
                file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
imp_list = dep_search(file_to_check,file_inform,file_and_package_names)

with open('file_info_t.txt', 'w') as file:
        file.write(str(imp_list))
        
with open("file_info_j.json", "w") as out_file:
        json.dump(str(imp_list), out_file, indent=6)
 
# print(f"all_files_name:{all_files}")
# print(f"all_files_and_package_name:{file_and_package_names}")
# print(f"files_inform:{file_inform}")
print(f"imp_list:{imp_list}")


           





