import os 
import json
import re
from glob import glob

import pandas as pd


def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content_y = file.readlines()
            content_y = [line.strip() for line in content_y  if line.startswith(("import","package"))]
            print(f"content is : {content_y}")
        return content_y
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

def extract_imports(content):
    try:
        imports = []
        print(f"extracted contents: {content}")
        for val in content:
            print(f"val in contents are: {val}")
            regex = r"(?:import\s+([\w]+(?:\.[\w]+)*)(?:\.\*|;)?)|((package)\s+([\w]+(?:\.[\w]+)?)\s*;)"
            matches = re.findall(regex,val)
            print(f"matches from content:{matches}")
            for match in matches:
                # print(f"match: {match}")
                module_name = match[0] or match[1]
                print(f"match: {match}")
                if "." in module_name:
                    module_name_ = module_name.split(".")[-1]
                    print(f"module name {module_name_}")
                    imports.append(module_name_)
                else:
                    print(f"else: match {module_name}")
                    imports.append(module_name)
        return list(set(imports))    
    except Exception as e:
        print(f"An error occured while extracting imports: {e}")
        return []
    


# def dep_search(file_to_check,content_val,seen=None):
#     if seen is None:
#         seen = []
#     imp_set = set()
#     print(f"content val {content_val}")
#     for i in content_val:
#         print(f"i of content val {i}")
#         print(f"i_file_name: {i['file_name']}")
#         if file_to_check in i["imp"] and i["file_name"] not in seen:
#             print(f"package value check:  {i['imp'][0]}")
#             imp_set.add(i["file_name"])
#             seen.append(i["file_name"])
#     #     elif "package" in i['imp'][0]:
#     #         print(f"package_file_name: {i['file_name']} and imp _name {i['imp']}")
#     # print(f"seen in list : {seen}")
#     seen_rec = set()
#     # print(f"imp_files: {imp_set}")
#     for imp_file in list(imp_set):
#         # print(f"imp_files: {imp_file}")
#         if imp_file not in seen_rec:
#             seen_rec.add(imp_file)
#             print(f"seen_rec: {seen_rec}")
#             imp_set.update(dep_search(imp_file, content_val, seen))

#     return list(imp_set)




def dep_search(file_to_check, files_inform, folder_inform,seen=None):
    dependencies = set()
    seen = set()
    seen_rec = set()
    parent_folder = None
    for folder in folder_inform:
        # print(f"folder name : {folder_inform} ")
        if folder['folder_files'] == file_to_check:
            parent_folder = folder['folder_name']
            break 
    # print(f"parent_folder: {parent_folder}")
    for file_info in files_inform:
        if file_to_check in file_info['imp'] and file_info['file_name'] not in seen:
            dependencies.add(file_info['file_name'])  # Direct dependency
    
    for imp_file in list(dependencies):
        # print(f"imp_files: {imp_file}")
        if imp_file not in seen_rec:
            seen_rec.add(imp_file)
            # print(f"seen_rec: {seen_rec}")
            dependencies.update(dep_search(imp_file,files_inform, seen))

    if parent_folder:
        for file_info in files_inform:
            if parent_folder in file_info['imp']:
                dependencies.add(file_info['file_name'])  


    return list(dependencies)




    
folder_path =  "C:\\Users\\LENOVO\\Desktop\\javaProdemo"

file_to_check = "MyClass"
file_inform = []
folder_inform = []
all_files = []
imp_list = []
extensions = ('.py','.js','.java')

if file_to_check.endswith(extensions):
    file_to_check = os.path.splitext(file_to_check)[0]#convert file without extension
        
for ext in extensions: 
    # print(f"ext is: {ext}")
    all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
    # print(f"all_files {all_files}")
for (dirpath,dirnames, filenames) in os.walk(folder_path):
    for file in filenames:
        if file.endswith(extensions):
            # print(f"file {file}")
            file_path = os.path.join(dirpath, file)
            file_contents = content_reader(file_path)
            # print(f"file:{file} file_contents: {file_contents}") # import as list of values
            if file_contents:
                file_imports = extract_imports(file_contents)
                # print(f"file {file} and file_imports {file_imports}")
                if "package" in file_imports[0]:
                    # print(f"package saved      {file} and file_imports {file_imports}")
                    package_name = file_imports[0].replace("package ", "").replace(";", "").strip()
                    # print(f"package name is  {package_name} {type(package_name)}")
                    folder_inform.append({"folder_name":package_name,"folder_files":file.split(".")[0]})
                else:    
                    file_inform.append({"file_name":file.split(".")[0],"imp":file_imports})
                # print(f"all files {all_files}")
        # print(f"file_inform {file_inform}")
imp_list = dep_search(file_to_check,file_inform,folder_inform)


        
with open('file_info_t.txt', 'w') as file:
    file.write(str(imp_list))
        
with open("file_info_j.json", "w") as out_file:
    json.dump(str(imp_list), out_file, indent=6)
    

# print(f"files_inform:{file_inform}")
# print(f"folder_inform:{folder_inform}")
print(f"imp_list:{imp_list}")


           




