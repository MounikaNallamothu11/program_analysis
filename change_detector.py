import re
from typing import List, Dict, Tuple
import os

def parse_java_elements(java_code: str) -> Dict[str, Tuple[str, str]]:
    elements = {}
    # Regular expressions to find class and method definitions
    class_regex = re.compile(r'\bclass\s+(\w+)')
    method_regex = re.compile(r'\b(public|private|protected|static|final|synchronized|native|abstract)?\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{')

    lines = java_code.splitlines()
    current_class = None


    inside_method = False
    method_name = ""
    method_signature = ""
    method_lines = []
    brace_count = 0

    for line in lines:

        class_match = class_regex.search(line)
        if class_match:
            current_class = class_match.group(1)


        method_match = method_regex.search(line)
        if method_match:
            if inside_method:
                elements[method_name] = (method_signature, "\n".join(method_lines).strip() + "\n}")  # Save the method signature and body

            # Start a new method
            inside_method = True
            method_name = f"{current_class}.{method_match.group(3)}"
            method_signature = f"{method_match.group(2)} {method_match.group(3)}({method_match.group(4)})"
            method_lines = [line.strip()]
            brace_count = 1

        elif inside_method:
            method_lines.append(line.strip())
            brace_count += line.count('{')
            brace_count -= line.count('}')

            if brace_count == 0:  # End of the current method
                inside_method = False
                elements[method_name] = (method_signature, "\n".join(method_lines).strip())  # Save the method signature and body

    return elements

def detect_changes_in_java_code(old_code: str, new_code: str, showBodies: bool = False) -> List[List[str]]:
    print("\nComparing Java code versions...\n")

    # Parse both versions of Java code
    old_elements = parse_java_elements(old_code)
    new_elements = parse_java_elements(new_code)

    affected_methods = []

    print("\nAffected methods:\n---------------------------------------------------------------------------------------------------------")
    for method_key, (old_signature, old_body) in old_elements.items():
        if method_key in new_elements:
            new_signature, new_body = new_elements[method_key]
            if old_body != new_body:
                affected_methods.append(method_key)
                print(f"Modified method: {method_key} | Old Signature: {old_signature} | New Signature: {new_signature}")
                if showBodies:
                    print(f"\nOld Body:\n----------------\n{old_body}\n")
                    print(f"New Body:\n----------------\n{new_body}\n\n")
    # Check for added and removed methods
    added_methods = set(new_elements.keys()) - set(old_elements.keys())
    removed_methods = set(old_elements.keys()) - set(new_elements.keys())

    if showBodies:
        print("New methods:\n---------------------------------------------------------------------------------------------------------")
    else:
        print("\n\nNew methods:\n---------------------------------------------------------------------------------------------------------")
    for method_key in added_methods:
        if showBodies:
            print(f"New method: {method_key} | Signature: {new_elements[method_key][0]} | Body:\n{new_elements[method_key][1]}\n")
        else:
            print(f"New method: {method_key} | Signature: {new_elements[method_key][0]}")

    if showBodies:
        print("\nRemoved methods:\n---------------------------------------------------------------------------------------------------------")
    else:
        print("\n\nRemoved methods:\n---------------------------------------------------------------------------------------------------------")
    for method_key in removed_methods:
        if showBodies:
            print(f"Removed method: {method_key} | Signature: {old_elements[method_key][0]} | Body:\n{old_elements[method_key][1]}\n")
        else:
            print(f"Removed method: {method_key} | Signature: {old_elements[method_key][0]}")
    
    print("\n")
    return [list(affected_methods), list(added_methods), list(removed_methods)]


def read_java_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


old_java_file_path = 'java/src/BankAccount.java'
new_java_file_path = 'temp/BankAccount.java'

old_java_code = read_java_file(old_java_file_path)
new_java_code = read_java_file(new_java_file_path)

[affected_methods, new_methods, removed_methods] = detect_changes_in_java_code(old_java_code, new_java_code, showBodies=False)

# print(f"Affected methods: {affected_methods}")
# print(f"New methods: {new_methods}")
# print(f"Removed methods: {removed_methods}\n")
