# task
"""Input:give a filename
Output: find the filenames that is import by the Input filename"""



import os
import json
import re
from glob import glob
import math_operation


folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 



def content_reader(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
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
        regex = r"(?:import\s+([\w\.]+)|from\s+([\w\.]+)\s+import)"
        imports = []
        
        matches = re.findall(regex, content)
        for match in matches:
            module_name = match[0] or match[1]
            imports.append(module_name)
        
        return imports
    except Exception as e:
        print(f"An error occurred while extracting imports: {e}")
        return []






def get_all_file_infos(folder_path, file_to_check):
    try:
        file_inform = {"file_name": None, "imported_files": []}
        all_files = []
        extensions = ('.py','.js',)

        if file_to_check.endswith(extensions):
            file_to_check = os.path.splitext(file_to_check)[0]
        
        for ext in extensions: 
            all_files.extend(os.path.splitext(os.path.basename(file))[0] for file in glob(os.path.join(folder_path, '**', f'*{ext}'), recursive=True))
        print(f"all_files {all_files}")
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            for file in filenames:
                if file.endswith(extensions):
                    print(f"file {file}")
                    file_path = os.path.join(dirpath, file)
                    file_contents = content_reader(file_path)
                    # print(f"file:{file} file_contents: {file_contents}")
                    
                    if file_contents:
                        file_imports = extract_imports(file_contents)
                        if file_to_check in file_imports:
                           file_inform["file_name"] = file_to_check 
                           file_inform["imported_files"].append(file)
        
        with open('file_info_t.txt', 'w') as file:
            file.write(str(file_inform))
        
        # Save the results to a JSON file
        with open("file_info_j.json", "w") as out_file:
            json.dump(file_inform, out_file, indent=6)
        
        return file_inform

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

if __name__ == "__main__":
    # folder_path = input("Enter the folder path: ")
    folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 
    file_to_check = input("Enter the file name to check: ")
    
    file_info = get_all_file_infos(folder_path, file_to_check)
    print(file_info)

