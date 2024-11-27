import os
import re


class DependencyTracker:
    class ASTNode:
        def __init__(self, type, name, children=None):
            self.type = type  # e.g., 'class', 'method', 'call'
            self.name = name
            self.children = children if children else []

        def add_child(self, child):
            self.children.append(child)

        def __repr__(self, level=0):
            ret = "\t" * level + f"{self.type}: {self.name}\n"
            for child in self.children:
                ret += child.__repr__(level + 1)
            return ret

    def __init__(self, project_folder: str) -> None:
        """
        Initializes the dependency tracker with the path to the Java project folder.
        """
        self.project_folder = project_folder
        self.user_defined_methods = set()
        self.classes = {}  # Map class name -> ASTNode (for cross-referencing)

    def read_java_files(self, folder: str) -> list[str]:
        """
        Read all Java files in the folder and its subdirectories.
        """
        java_files = []
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        java_files.append(f.read())
        return java_files

    def build_ast(self):
        """
        Build the AST for the entire project by parsing all Java files.
        """
        all_code = self.read_java_files(self.project_folder)

        # Root AST node for the entire project
        project_ast = self.ASTNode("project", "root")

        for code in all_code:
            parsed_ast = self.parse_java_code(code)
            project_ast.add_child(parsed_ast)

        return project_ast

    def parse_java_code(self, code: str) -> ASTNode:
        """
        Parse a single Java file to build an AST, resolving variable types for method calls on parameters
        and objects from collections.
        """
        lines = code.splitlines()
        root = self.ASTNode("file", "file-root")

        class_node = None
        method_node = None

        # Dictionary to track variable-to-class mappings
        variable_class_map = {}

        for line in lines:
            line = line.strip()

            # Check for class declaration
            class_match = re.match(r'(?:\b(public|private|protected)\s+)?\bclass\s+(\w+)', line)
            if class_match:
                class_name = class_match.group(2)
                class_node = self.ASTNode("class", class_name)
                root.add_child(class_node)
                self.classes[class_name] = class_node
                continue

            # Check for method declaration
            method_match = re.match(
                r'\b(public|private|protected|static|final|synchronized|native|abstract)?\s*(\b(public|private|protected|static|final|synchronized|native|abstract)\s+)*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{',
                line,
            )
            if method_match:
                method_name = method_match.group(5)
                method_params = method_match.group(6)  # Parameters inside parentheses
                method_node = self.ASTNode("method", method_name)
                if class_node:
                    self.user_defined_methods.add(f"{class_node.name}.{method_name}")
                    class_node.add_child(method_node)

                    # Parse method parameters and add them to the variable map
                    for param in method_params.split(","):
                        param = param.strip()
                        param_match = re.match(r'(\w+)\s+(\w+)', param)
                        if param_match:
                            param_type = param_match.group(1)  # Type of the parameter (e.g., `BankAccount`)
                            param_name = param_match.group(2)  # Name of the parameter (e.g., `destinationAccount`)
                            variable_class_map[param_name] = param_type
                continue

            # Check for instantiations (e.g., `ClassName obj = new ClassName(...)`)
            instantiation_match = re.search(
                r'\b([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)\s*=\s*new\s+([a-zA-Z_]\w*)\s*\(.*?\);',
                line
            )
            if instantiation_match and method_node:
                instantiated_class = instantiation_match.group(1)  # Class being instantiated
                variable_name = instantiation_match.group(2)  # Variable holding the instance
                constructor_call = self.ASTNode("call", f"{instantiated_class}.{instantiated_class}")  # Constructor call
                method_node.add_child(constructor_call)

                # Add variable-to-class mapping
                variable_class_map[variable_name] = instantiated_class
                continue

            # Check for method calls on variables (e.g., `obj.method(...)`)
            variable_method_call_match = re.search(r'\b([a-zA-Z_]\w*)\.(\w+)\s*\((.*?)\)', line)
            if variable_method_call_match and method_node:
                variable_name = variable_method_call_match.group(1)  # Variable calling the method
                method_name = variable_method_call_match.group(2)  # Method being called

                # Look up the class associated with the variable
                if variable_name in variable_class_map:
                    associated_class = variable_class_map[variable_name]
                    call_node = self.ASTNode("call", f"{associated_class}.{method_name}")
                    # Avoid duplicate calls
                    if not any(child.name == call_node.name for child in method_node.children):
                        method_node.add_child(call_node)
                continue

            # Handle enhanced for-loops (e.g., `for (ClassName var : collection)`)
            enhanced_for_loop_match = re.search(r'for\s*\(\s*(\w+)\s+(\w+)\s*:\s*(\w+)\s*\)', line)
            if enhanced_for_loop_match:
                iterated_class = enhanced_for_loop_match.group(1)  # Type of the iterated variable (e.g., `BankAccount`)
                iterated_var = enhanced_for_loop_match.group(2)  # Name of the iterated variable (e.g., `account`)
                variable_class_map[iterated_var] = iterated_class  # Map the variable to its class
                continue

            # Check for standalone method calls within the same class (e.g., `method(...)`)
            standalone_call_match = re.search(r'\b(\w+)\s*\((.*?)\)\s*;', line)
            if standalone_call_match and method_node:
                method_name = standalone_call_match.group(1)
                # If standalone, assume the call is within the same class
                caller_class = class_node.name if class_node else "UnknownClass"
                call_node = self.ASTNode("call", f"{caller_class}.{method_name}")
                # Avoid duplicate calls
                if not any(child.name == call_node.name for child in method_node.children):
                    method_node.add_child(call_node)

        return root



    def extract_callers(self, target_methods: set[str], project_ast: ASTNode) -> set[str]:
        """
        Extract all methods that call the given target methods.
        """
        callers = set()

        def find_callers(target_method, target_class, current_ast_node):
            for file_node in current_ast_node.children:
                if file_node.type == "file":  # Look into files
                    for class_node in file_node.children:  # Check each class within a file
                        if class_node.type == "class":
                            current_class = class_node.name
                            for method_node in class_node.children:
                                if method_node.type == "method":
                                    full_method_name = f"{current_class}.{method_node.name}"
                                    for child in method_node.children:
                                        if child.type == "call" and child.name == target_class + "." + target_method:
                                            # Ensure it matches the class context
                                            if target_class == current_class or child.name.startswith(target_class):
                                                callers.add(full_method_name)

        # Process each target method
        for method in target_methods:
            class_name, method_name = method.split('.')
            find_callers(method_name, class_name, project_ast)

        return callers

    def provide_all_caller_methods(self, methods: list[str], printAST: bool = False) -> set[str]:
        """
        Provide all methods that call the given list of methods.
        """
        # Build the AST for the entire project
        project_ast = self.build_ast()

        # Filter out non-user-defined methods
        filtered_ast = self.filter_non_user_defined_methods(project_ast)

        if printAST:
            print("\nAST Tree:\n")
            print(filtered_ast)

        # Extract caller methods
        return self.extract_callers(set(methods), filtered_ast)

    def filter_non_user_defined_methods(self, root: ASTNode) -> ASTNode:
        """
        Filters out non-user-defined calls from the AST while retaining user-defined methods and their valid structure.
        """
        def dfs(node):
            # If this is a 'call' node and not in user-defined methods, remove it
            if node.type == "call" and node.name not in self.user_defined_methods:
                return None
            elif node.type == "method" or node.type == "class" or node.type == "file" or node.type == "project":
                # Keep traversing for classes, methods, and files
                node.children = [dfs(child) for child in node.children if dfs(child)]
                return node
            # Retain other nodes by default (e.g., classes, methods, files)
            return node

        return dfs(root)

if __name__ == "__main__":
    # Example usage: Analyze a Java project
    project_folder = "java/modified/src"
    tracker = DependencyTracker(project_folder)

    # Specify target methods to analyze
    target_methods = ["BankAccount.withdraw"]

    # Get all caller methods
    caller_methods = tracker.provide_all_caller_methods(target_methods)
    print(f"Methods calling {target_methods}: {caller_methods}")