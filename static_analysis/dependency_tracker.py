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


    def __init__(self, modified_java_file_path: str = 'java/modified/src/BankAccount.java', modified_tests_file_path: str = 'java/modified/test/BankAccountTest.java') -> None:
        """
        Intializes the dependency tracker with the paths to the modified Java code and test files
        """
        self.modified_code = self.read_java_file(modified_java_file_path)
        self.modified_tests = self.read_java_file(modified_tests_file_path)
        self.user_defined_methods = set()


    def read_java_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()


    def provide_all_caller_methods(self, methods: list[str]):
        # Parse the modified code into an AST
        modified_ast = self.parse_java_code(self.modified_code)

        # Filter out non-user-defined methods
        modified_ast = self.filter_non_user_defined_methods(modified_ast)

        # Extract all caller methods
        all_caller_methods = self.extract_callers(methods, modified_ast)

        return all_caller_methods


    def filter_non_user_defined_methods(self, root: ASTNode):
        """
        Filters out non-user-defined methods from the AST.
        """
        def dfs(node):
            if node.type == "call" and node.name not in self.user_defined_methods:
                return None
            else:
                node.children = [child for child in node.children if dfs(child)]
                return node

        return dfs(root)


    def parse_java_code(self, code):
        """
        Parses Java code to build an AST.
        """
        lines = code.splitlines()
        root = self.ASTNode("root", "root")

        class_node = None
        method_node = None
        for line in lines:
            line = line.strip()

            # Check for class declaration
            class_match = re.match(r'(?:\b(public|private|protected)\s+)?\bclass\s+(\w+)', line)
            if class_match:
                class_name = class_match.group(2)
                class_node = self.ASTNode("class", class_name)
                root.add_child(class_node)
                continue

            # Check for method declaration
            method_match = re.match(r'\b(public|private|protected|static|final|synchronized|native|abstract)?\s*(\b(public|private|protected|static|final|synchronized|native|abstract)\s+)*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{', line)
            if method_match:

                # FOR NOW, WE ARE NOT PASSING WHOLE SIGNATURE TO METHOD NAME
                #method_name = method_match.group(5) + '(' + method_match.group(6) + ')'

                method_name = method_match.group(5)
                method_node = self.ASTNode("method", method_name)
                if class_node:
                    self.user_defined_methods.add(method_name)
                    class_node.add_child(method_node)
                continue

            # Check for method calls
            call_match = re.search(r'\b(\w+)\.(\w+)\s*\((.*?)\)', line)
            if call_match and method_node:
                method_name = call_match.group(2)
                call_node = self.ASTNode("call", method_name)
                method_node.add_child(call_node)

            standalone_call_match = re.search(r'\b(\w+)\s*\((.*?)\)\s*;', line)
            if standalone_call_match and method_node:
                method_name = standalone_call_match.group(1)
                call_node = self.ASTNode("call", method_name)
                method_node.add_child(call_node)
        
        return root


    def extract_callers(self, target_methods: set[str], code_ast) -> set[str]:
        """
        Extract all methods that call the given target methods.
        Input and output are sets to ensure uniqueness and efficiency.
        Returns callers in the format 'ClassName.methodName'.
        """
        callers = set()

        def find_callers(target_method, target_class):
            for class_node in code_ast.children:
                if class_node.type == "class":
                    current_class = class_node.name
                    for method_node in class_node.children:
                        if method_node.type == "method":
                            full_method_name = f"{current_class}.{method_node.name}"
                            for child in method_node.children:
                                if child.type == "call" and child.name == target_method:
                                    if target_class == current_class or child.full_name.startswith(target_class):
                                        callers.add(full_method_name)

        for method in target_methods:
            class_name, method_name = method.split('.')
            find_callers(method_name, class_name)

        return callers



if __name__ == "__main__":
    # Input: File paths for the modified code and unit tests
    modified_code_path = "BankAccount.java"  # Replace with your file path
    unit_test_path = "BankAccountTest.java"  # Replace with your file path

    # Perform static analysis
    #relevant_tests = static_analysis(modified_code_path, unit_test_path)
    #print("Relevant Unit Tests:", relevant_tests)
