import re
from typing import List, Dict, Tuple, Set
import os


class ChangeDetector:

    def __init__(self, old_project_path: str = "java/original/", new_project_path: str = "java/modified/"):
        """
        Initialize the ChangeDetector object with paths to the old and new project directories.
        """
        self.old_project_path = old_project_path
        self.new_project_path = new_project_path

    def parse_java_elements(self, java_code: str) -> Dict[str, Tuple[str, str, bool]]:
        """
        Parse Java code to extract classes and methods with their bodies and test classification.
        Returns a dictionary where keys are method names, and values are tuples containing:
        - method signature
        - method body
        - a boolean indicating whether the method is a test
        """
        elements = {}
        # Regular expressions to find class and method definitions
        class_regex = re.compile(r'\bclass\s+(\w+)')
        method_regex = re.compile(
            r'\b(public|private|protected|static|final|synchronized|native|abstract)?\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{')

        lines = java_code.splitlines()
        current_class = None

        inside_method = False
        method_name = ""
        method_signature = ""
        method_lines = []
        brace_count = 0
        is_test = False

        for i, line in enumerate(lines):
            line = line.strip()  # Trim whitespace

            # Check for class declarations
            class_match = class_regex.search(line)
            if class_match:
                current_class = class_match.group(1)

            # Detect @Test annotation
            if line == "@Test":
                is_test = True

            # Detect method declarations
            method_match = method_regex.search(line)
            if method_match:
                if inside_method:  # If already parsing a method, finalize the previous one
                    elements[method_name] = (
                        method_signature,
                        "\n".join(method_lines).strip(),
                        is_test
                    )
                # Start a new method
                inside_method = True
                method_name = f"{current_class}.{method_match.group(3)}"
                method_signature = f"{method_match.group(2)} {method_match.group(3)}({method_match.group(4)})"
                method_lines = [line]
                brace_count = 1
            elif inside_method:
                method_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:  # End of method
                    inside_method = False
                    elements[method_name] = (
                        method_signature,
                        "\n".join(method_lines).strip(),
                        is_test
                    )
                    is_test = False

        return elements

    def detect_changes(self, printer: bool = False, showBodies: bool = False) -> Dict[str, Set[str]]:
        """
        Detect changes in methods and tests across the project.
        Returns dictionaries of modified, added, and removed methods and tests.
        """
        print("\nComparing Java code versions...\n") if printer else None

        old_elements, new_elements = self.scan_project_files()

        # Detect added, removed, and modified methods
        added_methods = set(new_elements.keys()) - set(old_elements.keys())
        removed_methods = set(old_elements.keys()) - set(new_elements.keys())
        modified_methods = {
            method for method in set(old_elements.keys()) & set(new_elements.keys())
            if old_elements[method][1] != new_elements[method][1]
        }

        # Identify test changes
        added_tests = {method for method in added_methods if new_elements[method][2]}
        removed_tests = {method for method in removed_methods if old_elements[method][2]}
        modified_tests = {
            method for method in modified_methods
            if old_elements[method][2] or new_elements[method][2]
        }

        # Exclude tests from methods categories
        added_methods -= added_tests
        removed_methods -= removed_tests
        modified_methods -= modified_tests

        # Print changes if requested
        self.print_changes("New methods", added_methods, new_elements, showBodies, printer)
        self.print_changes("Removed methods", removed_methods, old_elements, showBodies, printer)
        self.print_changes("Modified methods", modified_methods, old_elements, showBodies, printer)
        self.print_changes("New tests", added_tests, new_elements, showBodies, printer)
        self.print_changes("Removed tests", removed_tests, old_elements, showBodies, printer)
        self.print_changes("Modified tests", modified_tests, old_elements, showBodies, printer)

        return {
            "added_methods": added_methods,
            "removed_methods": removed_methods,
            "modified_methods": modified_methods,
            "added_tests": added_tests,
            "removed_tests": removed_tests,
            "modified_tests": modified_tests
        }



    def scan_project_files(self) -> Tuple[Dict[str, Tuple[str, str, bool]], Dict[str, Tuple[str, str, bool]]]:
        """
        Scan all Java files in old and new project directories and parse their elements.
        """
        def collect_java_files(base_path):
            java_files = {}
            for dirpath, _, filenames in os.walk(base_path):
                for filename in filenames:
                    if filename.endswith(".java"):
                        file_path = os.path.join(dirpath, filename)
                        java_files[file_path] = self.read_java_file(file_path)
            return java_files

        old_files = collect_java_files(self.old_project_path)
        new_files = collect_java_files(self.new_project_path)

        old_elements = {}
        new_elements = {}

        for file_path, content in old_files.items():
            old_elements.update(self.parse_java_elements(content))

        for file_path, content in new_files.items():
            new_elements.update(self.parse_java_elements(content))

        return old_elements, new_elements

    def print_changes(self, title: str, changes: Set[str], elements: Dict[str, Tuple[str, str, bool]], showBodies: bool, printer: bool):
        """
        Helper function to print changes.
        """
        if changes:
            print(f"\n{title}:\n{'-' * 90}") if printer else None
            for method in changes:
                if method in elements:
                    signature, body, _ = elements[method]
                    print(f"{method} | Signature: {signature}") if printer else None
                    if showBodies:
                        print(f"Body:\n{body}\n{'-' * 90}") if printer else None

    def read_java_file(self, file_path: str) -> str:
        """
        Read the content of a Java file.
        """
        with open(file_path, 'r') as file:
            return file.read()


if __name__ == "__main__":
    detector = ChangeDetector()
    changes = detector.detect_changes(printer=True, showBodies=False)

    print("\nSummary of changes:")
    for change_type, methods in changes.items():
        print(f"{change_type.capitalize()}: {methods}")