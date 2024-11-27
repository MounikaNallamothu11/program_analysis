import os
from subprocess import Popen, PIPE
import re
import shutil
import json
import subprocess

class DynamicJavaAnalyzer:
    def __init__(self, project_path, static_analysis_results):
        self.src_path = project_path + "/src"  # Path to the class that needs to be tested
        self.test_path = project_path + "/test"  # Path to the JUnit test class
        self.project_path = project_path
        self.static_analysis_results = static_analysis_results
        self.original_json_mapping_path = "dynamic_analysis/dynamic_analysis_output.json"  # Path to the original JSON mapping
        self.test_answers = []

    def get_java_files(self, directory):
        """
            Recursively collects all `.java` files in the given directory.
            Returns a dictionary mapping filenames to their full paths.
            """
        java_files = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".java"):
                    full_path = os.path.normpath(os.path.join(root, file))
                    java_files[file] = full_path  # Map filename to full path
        return java_files


    def backup_and_restore(self, java_files, backup=True):
        """
        Backups or restores Java files based on the `backup` flag.
        """
        for filename, file_path in java_files.items():
            backup_path = f"{file_path}.bak"
            if backup:
                shutil.copy(file_path, backup_path)
                # print(f"Backup created for {filename}: {backup_path}")
            else:
                shutil.copy(backup_path, file_path)
                # print(f"Restored original file from {backup_path}")


    def restore_original_file(self,path,backup):
        """
        Restores the original class file from the backup.
        """
        if os.path.exists(backup):
            shutil.copy(backup, path)

    def insert_logging_statements(self, java_files):
        """
        Adds logging print statements to each method inside the given Java files.
        """
        # print(f"java_files: {java_files}")
        method_pattern = re.compile(r'(\b(public|private|protected|static|void|\s)*\s[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\))\s*\{')

        for file_path in java_files:
            with open(file_path, 'r') as file:
                code_lines = file.readlines()

            modified_code = []
            in_method = False
            for line in code_lines:
                method_match = method_pattern.search(line)
                if method_match:
                    method_name = method_match.group(0).split('(')[0].split()[-1]
                    modified_code.append(line)
                    modified_code.append(f'System.out.println("CALL {method_name}");\n')
                    in_method = True
                elif in_method and '}' in line:
                    modified_code.append(line)
                    in_method = False
                else:
                    modified_code.append(line)

            with open(file_path, 'w') as file:
                file.writelines(modified_code)


    def compile_and_run_tests(self, test_methods=None):
        """
        Compiles and runs the modified class under test, along with the JUnit test class, using Maven.
        If test_methods is provided, only those tests will be run.
        """
        current_directory = os.getcwd()
        os.chdir(self.project_path)

        try:
            if test_methods:
                # Construct the Maven command to run specific test methods
                self.test_answers.extend(test_methods)
                self.test_answers = list(dict.fromkeys(self.test_answers))
                combined_tests = "+".join(sorted(set(test_methods)))
                print(f"Running required tests: {combined_tests}")
                maven_command = ['mvn', 'test', f'-Dtest=BankAccountTest#{combined_tests}']
            else:
                # Default Maven command to run all tests
                print("Running all tests...")
                maven_command = ['mvn','test']

            # Run the Maven command and capture output
            # result = subprocess.run(maven_command, text=True, capture_output=True, check=True)
            process = Popen(maven_command,stdout=PIPE, stderr=PIPE, shell=True)
            result, stderr = process.communicate()

            # Check the result and handle errors
            if process.returncode != 0:
                print("Maven build and test failed with errors:")
                print(result)
                return None

            # Return the stdout (test results) for further analysis

            print(result.decode())
            return result.decode()

        except subprocess.CalledProcessError as e:
            # Handle subprocess errors globally
            print(f"Error running Maven command: {e.stderr}")
            return None

        finally:
            self.cleanup()
            os.chdir(current_directory)


    def extract_class_names(self, java_files):
        """
        Extracts class names from a dictionary of Java files, where the key is the filename
        and the value is the file path. Returns a dictionary of {java_file: class_name}.
        """
        class_names = {}

        # Regular expression to match class declarations (public, private, protected modifiers are allowed)
        class_pattern = re.compile(r'\b(class)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{]')

        # Iterate over the dictionary items (filename: path)
        for java_file, file_path in java_files.items():
            # Convert relative paths to absolute paths
            java_file_path = os.path.abspath(file_path)

            # Check if the file exists before trying to open it
            if not os.path.exists(java_file_path):
                print(f"Warning: File {java_file_path} does not exist!")
                continue

            # Now extract the class name
            class_name = self.get_class_name_from_file(java_file_path)

            if class_name:
                class_names[java_file] = class_name

            # print(f"Class names so far: {class_names}")

        return class_names


    def get_class_name_from_file(self, file_path):
        """
        Extracts the class name from the Java file at the given path.
        """
        class_pattern = re.compile(r'\b(class)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[{]')
        class_name = None

        # Open the file to read its content
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                match = class_pattern.search(line)
                if match:
                    class_name = match.group(2)  # The class name is the second capture group
                    break  # Stop after finding the first class name

        return class_name


    def parse_output(self, output, class_names):
        """
        Parses the output from the test run to associate each test with the methods it calls.
        Ignores the class name as a method, and avoids repeating method names for each test.
        """
        method_calls = {}
        current_test_method = None

        for line in output.splitlines():
            # Detect start of a test method based on its name (assuming test methods start with "CALL test")
            if line.startswith("CALL test"):
                current_test_method = line.split("CALL ")[1]
                method_calls[current_test_method] = set()  # Use a set to avoid repeating method names
            elif line.startswith("CALL"):
                # If it's a method call, add it to the current test method's list
                method_name = line.split("CALL ")[1]

                # Ensure we do not add the class name as a method
                if method_name not in class_names.values() and current_test_method:
                    method_calls[current_test_method].add(method_name)  # Use set to avoid duplicates

        # Convert sets back to lists to maintain the expected output format
        method_calls = {test: list(calls) for test, calls in method_calls.items()}

        return method_calls

    def delete_backup(self,path):
        """
        Deletes the backup file after the operation is complete.
        """
        if os.path.exists(path):
            os.remove(path)

    def cleanup(self):
        """
        Restores the original Java files and deletes their backups.
        """
        # Collect all Java files from the src and test directories
        all_java_files = self.get_java_files(self.src_path)
        all_java_files.update(self.get_java_files(self.test_path))  # Merge src and test files

        # print("Restoring original files from backups...")
        for filename, full_path in all_java_files.items():
            backup_path = full_path + ".bak"
            # print(f"Restoring {filename} from {backup_path}...")
            self.restore_original_file(full_path, backup_path)

        # print("Deleting backup files...")
        for filename, full_path in all_java_files.items():
            backup_path = full_path + ".bak"
            # print(f"Deleting backup for {filename} at {backup_path}...")
            self.delete_backup(backup_path)

        # print("Cleanup completed.")

    def save_results_to_json(self, results):
        # Reverse the mapping: call → test_methods
        reversed_mapping = {}
        for test_method, calls in results.items():
            for call in calls:
                if call not in reversed_mapping:
                    reversed_mapping[call] = []
                reversed_mapping[call].append(test_method)

        # Save or print the JSON
        with open(self.original_json_mapping_path, "w") as json_file:
            json.dump(reversed_mapping, json_file, indent=4)

        print(f"Results saved to {self.original_json_mapping_path}")
        print(json.dumps(reversed_mapping, indent=4))


    def load_existing_mapping(self):
        """
        Loads the existing JSON mapping (if it exists), or creates a new one.
        """
        original_json_mapping_path = "dynamic_analysis/dynamic_analysis_output.json"
        if os.path.exists(original_json_mapping_path):
            with open(original_json_mapping_path, 'r') as f:
                return json.load(f)
        else:
            print("No existing JSON mapping found, creating a new one.")
            return []  # Return an empty list if no mapping file exists

    def extract_method_name(self, full_name):
        """
        Extracts the method name from a fully qualified method name.
        """
        return full_name.split('.')[-1]

    def analyze(self):
        # Collect Java files from both src and test directories
        all_java_files = self.get_java_files(self.src_path)
        all_java_files.update(self.get_java_files(self.test_path))  # Merge dictionaries

        # Backup original files
        self.backup_and_restore(all_java_files, backup=True)

        # print(f"Current working directory: {os.getcwd()}")
        original_json_mapping_path = "dynamic_analysis/dynamic_analysis_output.json"

        # Check if existing mapping is present
        # print(original_json_mapping_path)
        if os.path.exists(original_json_mapping_path):
            print("Existing mapping found. Loading the mapping...")
            existing_mapping = self.load_existing_mapping()
            method_calls = {}

            if self.static_analysis_results:
                print(f"Static analysis results found: {self.static_analysis_results}")
                # Segregate affected methods and tests
                modified_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("directly_affected_methods", set())}
                removed_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("removed_methods", set())}
                added_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("added_methods", set())}
                added_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("added_tests", set())}
                modified_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("modified_tests", set())}
                removed_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("removed_tests", set())}

                # Remove entries of removed methods
                for removed_method in removed_methods:
                    if removed_method in existing_mapping:
                        del existing_mapping[removed_method]

                # Remove entries of removed tests
                for test in removed_tests:
                    for method in list(existing_mapping.keys()):
                        if test in existing_mapping[method]:
                            existing_mapping[method].remove(test)
                        if not existing_mapping[method]:  # Remove method if no tests remain
                            del existing_mapping[method]

                # Save updated mapping to JSON
                with open(original_json_mapping_path, "w") as json_file:
                    json.dump(existing_mapping, json_file, indent=4)

                # Run new and modified tests
                tests_to_run = added_tests.union(modified_tests)
                if tests_to_run:
                    for full_path in all_java_files.values():
                        self.insert_logging_statements([full_path])

                    output = self.compile_and_run_tests(list(tests_to_run))
                    if output is None:
                        print("Error occurred while running new/modified tests.")
                        return

                    class_names = self.extract_class_names(all_java_files)
                    method_calls = self.parse_output(output,class_names)
                    self.cleanup()
                    self.save_results_to_json(method_calls)

                # Check for affected methods and run relevant tests
                affected_methods = added_methods.union(modified_methods)
                affected_methods_testMethods_Mapping = {}

                for method, test_methods in existing_mapping.items():
                    if method in affected_methods:
                        affected_methods_testMethods_Mapping [method] = test_methods


                if affected_methods_testMethods_Mapping :
                    test_methods_to_run = list({test for tests in affected_methods_testMethods_Mapping .values() for test in tests})
                    self.compile_and_run_tests(test_methods_to_run)

            print(f"The affected test cases are: {self.test_answers}")
            print("Analysis complete.")
            self.cleanup()
            return

        else:
            # If no existing mapping, create a new one
            print("No existing mapping found. Creating a new one...")
            method_calls = {}

            # Insert logging into all Java files
            # print("Inserting logging statements into all relevant Java files...")
            for full_path in all_java_files.values():
                self.insert_logging_statements([full_path])

            # print("Compiling and running all Java files...")
            output = self.compile_and_run_tests()
            if output is None:
                return

            class_names = self.extract_class_names(all_java_files)

            # print("Parsing output to determine method calls...")
            method_calls = self.parse_output(output, class_names)

            self.cleanup()


            self.save_results_to_json(method_calls)

            print("Analysis complete.")

            return




if __name__ == "__main__":
    # Static analysis results: List of methods that were changed (for example)
    #static_analysis_results = {
    #    "directly_affected_methods": {
    #       "BankAccount.deposit",
    #       "BankAccount.withdraw",
    #        "BankAccount.calculateInterest",
    #       "BankAccount.transfer",
    #       "BankAccount.sumPositiveBalances"
    #   },
    #    "added_methods": {
    #        "BankAccount.getAccountSummary"
    #    },
    #    "removed_methods": {
    #       "BankAccount.calculateInterestDivideByZero"
    #    },
    #    "added_tests": {
    #        "BankAccountTest.testGetAccountSummary"
    #    },
    #    "modified_tests": {
    #        "BankAccountTest.testTransferSuccess"
    #    },
    #    "removed_tests": {
    #        "BankAccountTest.testCalculateInterestDivideByZero"
    #    }
   # }
    #src_path = "java/original/src/main"  # Path to the class that needs to be tested
    #test_path = "java/original/test"  # Path to the JUnit test class
    #project_path = "java/original"
    analyzer = DynamicJavaAnalyzer(project_path, static_analysis_results)
    results = analyzer.analyze()
    # analyzer.run_all_tests()