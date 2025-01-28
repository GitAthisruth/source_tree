import os 
import json
import re
from glob import glob

import pandas as pd




folder_path =  "C:\\Users\\LENOVO\\Desktop\\javaProdemo"

file_to_check = "MyClass"

file_inform = []
all_files = []
imp_list = []
file_and_package_names= []
extensions = ('.py','.js','.java')

if file_to_check.endswith(extensions):
    file_to_check = os.path.splitext(file_to_check)[0]
    print(f"file_to_check:{file_to_check}")
        
for ext in extensions: 
    print(f"ext is: {ext}")
    all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
    print(f"all_files {all_files}")
for (dirpath,dirnames, filenames) in os.walk(folder_path):
    print(f"dirpath:{dirpath} dirname:{dirnames} filename:{filenames}")#here we can check for the dir name if that is imported to any java files.then all the class are dependent to that file.
    for file in filenames:
        if file.endswith(extensions):
            # print(f"file {file}")
            file_path = os.path.join(dirpath, file)
            folder_name = os.path.split(dirpath)[-1]
            file_name = os.path.basename(file_path).split(".")[0]
            print(f"dirpath: {os.path.split(dirpath)[-1]}")
            print(f"file_path_:{file_path}")
            file_and_package_names.append({"folder_name": folder_name, "file_name": file_name})
# print(f"all_files_name:{all_files}")
# print(f"all_files_name:{file_and_package_names}")
            


