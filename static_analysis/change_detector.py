import re
from typing import List, Dict, Tuple
import os


class ChangeDetector:

    def __init__(self, old_project_path: str = "java/original/", new_project_path: str = "java/modified/"):
        """
        Initialize the ChangeDetector object with the paths to the old and new project directories
        """
        self.old_project_path = old_project_path
        self.new_project_path = new_project_path

    def parse_java_elements(self, java_code: str) -> Dict[str, Tuple[str, str]]:
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

        for line in lines:
            class_match = class_regex.search(line)
            if class_match:
                current_class = class_match.group(1)

            method_match = method_regex.search(line)
            if method_match:
                if inside_method:
                    elements[method_name] = (method_signature, "\n".join(
                        method_lines).strip() + "\n}")  # Save the method signature and body

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
                    elements[method_name] = (method_signature, "\n".join(
                        method_lines).strip())  # Save the method signature and body

        return elements

    def detect_changes(self, printer: bool = False, showBodies: bool = False) -> Tuple[set, set, set, set, set, set]:
        """
        Detect changes in methods and tests across the project.
        Returns modified, added, and removed methods and tests.
        """
        print("\nComparing Java code versions...\n") if printer else None

        old_elements, new_elements = self.scan_project_files()

        # Categorize changes
        modified_methods = set()
        added_methods = set(new_elements.keys()) - set(old_elements.keys())
        removed_methods = set(old_elements.keys()) - set(new_elements.keys())

        print("\nModified methods:\n" + "-" * 90) if printer else None
        for method_key, (old_signature, old_body) in old_elements.items():
            if method_key in new_elements:
                new_signature, new_body = new_elements[method_key]
                if old_body != new_body:
                    modified_methods.add(method_key)
                    print(f"Modified method: {method_key} | Old Signature: {old_signature} | New Signature: {new_signature}") if printer else None
                    if showBodies:
                        print(f"\nOld Body:\n{'-' * 16}\n{old_body}\n") if printer else None
                        print(f"New Body:\n{'-' * 16}\n{new_body}\n") if printer else None

        # Extract and filter test methods
        test_filter = lambda x: x.startswith("Test") or "Test" in x  # Test methods often have "Test" in their class name
        modified_tests = {method for method in modified_methods if test_filter(method)}
        added_tests = {method for method in added_methods if test_filter(method)}
        removed_tests = {method for method in removed_methods if test_filter(method)}

        # Print results
        self.print_changes("New methods", added_methods, new_elements, showBodies, printer)
        self.print_changes("Removed methods", removed_methods, old_elements, showBodies, printer)
        self.print_changes("Modified tests", modified_tests, old_elements, showBodies, printer)
        self.print_changes("New tests", added_tests, new_elements, showBodies, printer)
        self.print_changes("Removed tests", removed_tests, old_elements, showBodies, printer)

        # Create a dictionary to store results
        changes = {
            "modified_methods": modified_methods,
            "added_methods": added_methods,
            "removed_methods": removed_methods,
            "modified_tests": modified_tests,
            "added_tests": added_tests,
            "removed_tests": removed_tests
        }

        return changes

    def scan_project_files(self) -> Tuple[Dict[str, Tuple[str, str]], Dict[str, Tuple[str, str]]]:
        """
        Scan all Java files in both old and new project directories and parse their elements.
        """
        def collect_java_files(base_path):
            java_files = {}
            for dirpath, _, filenames in os.walk(base_path):
                for filename in filenames:
                    if filename.endswith(".java"):
                        file_path = os.path.join(dirpath, filename)
                        java_files[file_path] = self.read_java_file(file_path)
            return java_files

        old_java_files = collect_java_files(self.old_project_path)
        new_java_files = collect_java_files(self.new_project_path)

        old_elements = {}
        new_elements = {}

        for file_path, content in old_java_files.items():
            old_elements.update(self.parse_java_elements(content))

        for file_path, content in new_java_files.items():
            new_elements.update(self.parse_java_elements(content))

        return old_elements, new_elements

    def print_changes(self, title, changes, elements, showBodies, printer):
        if changes:
            print(f"\n{title}:\n" + "-" * 90) if printer else None
            for method_key in changes:
                if method_key in elements:
                    signature, body = elements[method_key]
                    print(f"{method_key} | Signature: {signature}") if printer else None
                    if showBodies:
                        print(f"Body:\n{body}\n") if printer else None

    def read_java_file(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read()


if __name__ == "__main__":
    detector = ChangeDetector()
    changes = detector.detect_changes(printer=True, showBodies=False)

    modified_methods = changes["modified_methods"]
    added_methods = changes["added_methods"]
    removed_methods = changes["removed_methods"]
    modified_tests = changes["modified_tests"]
    added_tests = changes["added_tests"]
    removed_tests = changes["removed_tests"]
    
    print(f"\n\nModified methods: {modified_methods}")
    print(f"Added methods: {added_methods}")
    print(f"Removed methods: {removed_methods}")
    print(f"Modified tests: {modified_tests}")
    print(f"Added tests: {added_tests}")
    print(f"Removed tests: {removed_tests}")
