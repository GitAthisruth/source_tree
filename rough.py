import re

# val = {"file":[]}

# val["file"].append({"file_name":"str.txt","file_path":"dhjdjd/djdk/djdk/"})
# val["file"].append({"file_name":"strrr.txt","file_path":"lofkjd/kkdlk/iror/"})




# print(val)

# reading files

# valr = "sjjkk sjkskjkj skskjjksd import bn import bn as hshjs import main.py sghd.js jdkd.js from ahhsjs import as hsjs "
# bn = "sajksaklklas jasjksa import valr import shjs.js hsjs.py"
# bnr = "ashjhas sajhjhsaj js.py sgsh.js"

# ls = {"valr": valr, "bn": bn, "bnr": bnr}

# for key, val in ls.items():
#     if "import" in val and key in val:
#         print(val)
#         print(f"{key} is imported in {val}")
    

# valr = "sjjkk sjkskjkj skskjjksd import bn "
# bn = "sajksaklklas jasjksa import valr"
# bnr = "ashjhas sajhjhsaj"

# ls = {"valr": valr, "bn": bn, "bnr": bnr}

# for key, val in ls.items():
#     for other_key in ls.keys():
#         if other_key != key and "import" in val and other_key in val:
#              print(f"{other_key} is imported in {key}")

# # content_dir = {'file_information': [{'file_name': 'main.py', 'file_path': 'C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree\\main.py', 'file_content': '# main.py\n\nimport math_operation\n\ndef main():\n    num1 = 10\n    num2 = 5\n\n    print("Addition:", math_operation.add(num1, num2))\n    print("Subtraction:", math_operation.subtract(num1, num2))\n    print("Multiplication:", math_operation.multiply(num1, num2))\n    print("Division:", math_operation.divide(num1, num2))\n\nif __name__ == "__main__":\n    main()\n'}, {'file_name': 'math_operation.py', 'file_path': 'C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree\\math_operation.py', 'file_content': 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\ndef divide(a, b):\n    if b != 0:\n        return a / b\n    else:\n        return "Cannot divide by zero"'}, {'file_name': 'main_subfolder.py', 'file_path': 'C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree\\sub_folder\\main_subfolder.py', 'file_content': '# main.py\n\nimport math_operation\n\ndef main():\n    num1 = 10\n    num2 = 5\n\n    print("Addition:", math_operation.add(num1, num2))\n    print("Subtraction:", math_operation.subtract(num1, num2))\n    print("Multiplication:", math_operation.multiply(num1, num2))\n    print("Division:", math_operation.divide(num1, num2))\n\nif __name__ == "__main__":\n    main()\n'}, {'file_name': 'math_operation_subfolder.py', 'file_path': 'C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree\\sub_folder\\math_operation_subfolder.py', 'file_content': 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\ndef divide(a, b):\n    if b != 0:\n        return a / b\n    else:\n        return "Cannot divide by zero"'}]}

# import os

# import ast 

# file_path =  "C:\\Users\\LENOVO\Desktop\\prizmora\\source_tree" 



# def finding_imports_and_file_names(content_dir):
#      for key, val in content_dir.items():
#           print(f"key:{key}")
#           for other_key in content_dir.keys():
#                if other_key != key and "import" in val and other_key in val:
#                     print(f"other_key:{other_key}")
#                     print(f"{other_key} is imported in {key}")
     


# def find_imports_in_file(file_path):
#     """Return a list of modules/files imported in a given Python file"""
#     imported_files = []
#     with open(file_path, "r") as file:
#         tree = ast.parse(file.read(), filename=file_path)
#         for node in ast.walk(tree):#searching for elements in a tree 
#             if isinstance(node, ast.Import):
#                 for n in node.names:# node.name represent the name after the node(eg:if import os the name is os)
#                     imported_files.append(n.name)
#             elif isinstance(node, ast.ImportFrom):
#                 imported_files.append(node.module)
#     return imported_files


# def finding_imports_and_file_names(content_dir):
#     for key, val in content_dir.items():
#         print(f"Checking file: {key}")
#         # Check the imports in the current file
#         imports_in_key = find_imports_in_file(val)
#         for other_key in content_dir.keys():
#             if other_key != key:
#                 # Check if 'other_key' is in the imports of 'key'
#                 if any(other_key in imp for imp in imports_in_key):
#                     print(f"{other_key} is imported in {key}")

# content_dir ={'main.py': '# main.py\n\nimport math_operation\n\ndef main():\n    num1 = 10\n    num2 = 5\n\n    print("Addition:", math_operation.add(num1, num2))\n    print("Subtraction:", math_operation.subtract(num1, num2))\n    print("Multiplication:", math_operation.multiply(num1, num2))\n    print("Division:", math_operation.divide(num1, num2))\n\nif __name__ == "__main__":\n    main()\n', 'math_operation.py': 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\ndef divide(a, b):\n    if b != 0:\n        return a / b\n    else:\n        return "Cannot divide by zero"', 'main_subfolder.py': '# main.py\n\nimport math_operation\n\ndef main():\n    num1 = 10\n    num2 = 5\n\n    print("Addition:", math_operation.add(num1, num2))\n    print("Subtraction:", math_operation.subtract(num1, num2))\n    print("Multiplication:", math_operation.multiply(num1, num2))\n    print("Division:", math_operation.divide(num1, num2))\n\nif __name__ == "__main__":\n    main()\n', 'math_operation_subfolder.py': 'import math_operation\n\ndef add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\ndef divide(a, b):\n    if b != 0:\n        return a / b\n    else:\n        return "Cannot divide by zero"', 'file1.py': 'def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b', 'file2.py': 'from file1 import add\n\ndef multiply(a, b):\n    return a * b\n\ndef main():\n    result = add(2, 3)\n    print(result)\n'}

# finding_imports_and_file_names(content_dir)



# content = "sjjkk sjkskjkj skskjjksd import bn import bn as hshjs import main sghd.js jdkd.js from ahhsjs import asdd hsjs "
# def extract_imports(content):
#     regex = r"(?:import\s+([\w\.]+)|from\s+([\w\.]+)\s+import)"
#     imports = []
    
#     # Use re.findall to find all matches in the content
#     matches = re.findall(regex, content)
#     for match in matches:
#         # Each match is a tuple; one of the elements will be None
#         module_name = match[0] or match[1]
#         imports.append(module_name)
    
#     return imports

# print(extract_imports(content))


# def extract_imports(content, file_to_check):
#     # Create a dynamic regex to match the specified file_to_check
#     regex = rf"(^|\s)(?:import\s+([\w\.]+)|from\s+([\w\.]+)\s+import)\s*({re.escape(file_to_check)})\.py"
    
#     imports = []
    
#     # Use re.findall to find all matches in the content
#     matches = re.findall(regex, content)
#     for match in matches:
#         # Extract the module name (either from 'import' or 'from ... import')
#         module_name = match[1] or match[2]
#         imports.append(module_name)
    
#     return imports

# # Example input
# valr = """
# import main.py
# from file1 import ahsh
# import math_operation
# from main import function
# from main.py import submodule
# """

# # Specify the file you want to check for, e.g., "main"
# file_to_check = "main"  # this can be dynamically passed as well

# # Extract imports for the specified file_to_check
# extracted_imports = extract_imports(valr, file_to_check)
# print(extracted_imports)



# import re

# def extract_imports(content, file_to_check):
#     # Create a dynamic regex pattern for various import formats
#     regex = rf"(?:import\s+([\w\.]+)(?:\s+as\s+[\w]+)?|from\s+([\w\.]+)\s+import\s+[\w\.\,]+)\s+{re.escape(file_to_check)}\b"
    
#     imports = []
    
#     # Use re.findall to find all matches
#     matches = re.findall(regex, content)
    
#     for match in matches:
#         # Extract the module name (either from 'import' or 'from ... import')
#         module_name = match[0] or match[1]
#         imports.append(module_name)
    
#     return imports

# Example input
# valr = """import main
# import math as m
# from math import sqrt
# from main import function1, function2"""

# # File to check (e.g., "main")
# file_to_check = "main"  # This is the dynamic file name you're searching for

# # Extract imports for the specified file_to_check
# extracted_imports = extract_imports(valr, file_to_check)
# print(extracted_imports)

import os 

# va = "python.py"

# extensions = ('.py', '.java', '.js', '.html')

# # va = os.path.basename(va)
# if va.endswith(extensions):
#     va = os.path.splitext(va)[0]

# print(va)


content = "import os import json import re from glob import glob import main"

folder_path =  "C:\\Users\\LENOVO\\Desktop\\prizmora\\source_tree" 

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
    

print(extract_imports(content))


'''output'''
dependency = {"file_name":"main","dep":["math","search","math_op","main_sub","file_1","file_2"],
            "file_name":"maths","dep":["search","file1","file2","main_sub","math_op"],
            "file_name":"search","dep":[],
            "file_name":"file1","dep":["file2"],
            "file_name":"file2","dep":[],
            "file_name":"main_sub","dep":[],
            "file_name":"math_op","dep":[]}

'''input'''

con = {"file_name":"main","dep":["os"],
            "file_name":"maths","dep":['main','pandas','sub_folder'],
            "file_name":"search","dep":['by', 'os', 'json', 're', 'glob', 'math_operation', 're'],
            "file_name":"file1","dep":['math_operation', 'main'],
            "file_name":"file2","dep":['file1'],
            "file_name":"main_sub","dep":['math_operation'],
            "file_name":"math_op","dep":['math_operation']}

