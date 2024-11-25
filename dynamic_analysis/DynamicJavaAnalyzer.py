import os
from subprocess import Popen, PIPE
import re
import shutil
import json
import subprocess

class DynamicJavaAnalyzer:
    def __init__(self, class_under_test_path, test_class_path, project_path, static_analysis_results):
        self.class_under_test_path = os.path.abspath(f"{class_under_test_path}")  # The class to be tested
        self.test_class_path = os.path.abspath(f"{test_class_path}")  # The JUnit test class path
        self.project_path = project_path
        self.static_analysis_results = static_analysis_results
        # Backup file path for restoring the original class after modifications
        self.backup_class_path = os.path.abspath(f"{class_under_test_path}.bak")
        self.backup_test_path = os.path.abspath(f"{test_class_path}.bak")
        self.class_name = os.path.basename(self.class_under_test_path).split('.')[0]
        self.original_json_mapping_path = "dynamic_analysis/dynamic_analysis_output.json"  # Path to the original JSON mapping

    def backup_original_file(self,path,backup):
        """
        Creates a backup of the original class file.
        """
        if not os.path.exists(backup):
            shutil.copy(path, backup)

    def restore_original_file(self,path,backup):
        """
        Restores the original class file from the backup.
        """
        if os.path.exists(backup):
            shutil.copy(backup, path)

    def insert_logging_statements(self,path):
        """
        Adds logging print statements to each method inside the class under test.
        The print statement is added as the first line inside each method body.
        """
        # Load the original class under test content
        with open(path, 'r') as file:
            class_code = file.readlines()

        # Regex to identify method signatures (excluding the method body)
        method_pattern = re.compile(r'(\b(public|private|protected|static|void|\s)*\s[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\))\s*\{')

        modified_code = []
        in_method = False

        for line in class_code:
            method_match = method_pattern.search(line)
            if method_match:
                # If we found a method, insert the print statement immediately after the opening brace '{'
                method_name = method_match.group(0).split('(')[0].split()[-1]  # Extract method name
                modified_code.append(line)  # Add method declaration
                modified_code.append(f'System.out.println("CALL {method_name}");\n')  # Insert print inside method body
                in_method = True
            elif in_method:
                # Check for the closing brace '}' for the current method
                if '}' in line:
                    modified_code.append(line)
                    in_method = False
                else:
                    modified_code.append(line)
            else:
                modified_code.append(line)

        # Write the modified code to the original file
        with open(path, 'w') as file:
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
                # Extract unique test methods
                combined_tests = "+".join(sorted(set(test_methods)))

                maven_command = ['mvn', 'test', f'-Dtest=BankAccountTest#{combined_tests}']
                print(f"Running required tests: {combined_tests}")

                try:
                    # Run the Maven command and capture output
                    result = subprocess.run(maven_command, text=True, capture_output=True, check=True)
                    print(result.stdout)  # Display Maven output
                except subprocess.CalledProcessError as e:
                    print(f"Error running required tests: {e.stderr}")
            else:
                # Default Maven command to run all tests
                print("Running all tests...")
                maven_command = ['mvn', 'clean', 'test']

            # Execute the Maven command
            result = subprocess.run(
                maven_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if result.returncode != 0:
                print("Maven build and test failed with errors:")
                print(result.stderr)
                return None

            # Return the stdout (test results) for further analysis
            print(result.stdout)
            return result.stdout

        finally:
            self.cleanup()
            os.chdir(current_directory)


    def parse_output(self, output):
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
                if method_name != self.class_name and current_test_method:
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
        Restores the original class and test files and deletes their backups.
        """
        print("Restoring the original class file...")
        self.restore_original_file(self.class_under_test_path, self.backup_class_path)

        print("Restoring the original test file...")
        self.restore_original_file(self.test_class_path, self.backup_test_path)

        print("Deleting class backup file...")
        self.delete_backup(self.backup_class_path)

        print("Deleting test backup file...")
        self.delete_backup(self.backup_test_path)


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
        # Backup original files
        print("Backing up the original class file...")
        self.backup_original_file(self.class_under_test_path, self.backup_class_path)

        print("Backing up the original test file...")
        self.backup_original_file(self.test_class_path, self.backup_test_path)

        print(f"Current working directory: {os.getcwd()}")
        original_json_mapping_path = "dynamic_analysis/dynamic_analysis_output.json"

        # Check if existing mapping is present, else create a new one
        print(original_json_mapping_path)
        if os.path.exists(original_json_mapping_path):
            print("Existing mapping found. Loading the mapping...")
            existing_mapping = self.load_existing_mapping()
            method_calls = {}

            if self.static_analysis_results:
                print(f"Static analysis results found: {self.static_analysis_results}")
                # If there are changes from static analysis, filter tests based on changed methods
                #TODO start
                # seggregate, affected methods, removed methods, new tests, modified tests and remove tests
                # Then, remove removed methods and testcases mapped with it, remove removed tests from the existing mapping.
                #Now Run the new tests and modified tests and append the method to tests mapping in the existing mapping(Follow logging technique for tracing methods that I used for first generating json)
                #TODO end
                # Segregate affected methods and tests
                modified_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("Modified_methods", set())}
                removed_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("Removed_methods", set())}
                added_methods = {self.extract_method_name(method) for method in self.static_analysis_results.get("Added_methods", set())}
                added_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("Added_tests", set())}
                modified_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("Modified_tests", set())}
                removed_tests = {self.extract_method_name(test) for test in self.static_analysis_results.get("Removed_tests", set())}

                # Remove entries of removed methods
                for removed_method in removed_methods:
                    if removed_method in existing_mapping:
                        del existing_mapping[removed_method]

                # Remove entries of removed tests
                for test in removed_tests:
                    for method in list(existing_mapping.keys()):  # Iterate over keys (methods)
                        if test in existing_mapping[method]:
                            existing_mapping[method].remove(test)  # Remove the test
                        # Remove the method if no tests remain
                        if not existing_mapping[method]:
                            del existing_mapping[method]

                # Save the updated mapping back to the JSON file
                with open(original_json_mapping_path, "w") as json_file:
                    json.dump(existing_mapping, json_file, indent=4)
                # Run new and modified tests and update mapping
                tests_to_run = added_tests.union(modified_tests)
                if tests_to_run:
                    print(f"Running new and modified tests: {tests_to_run}")
                    # Add logging to trace new/modified test executions
                    self.insert_logging_statements(self.class_under_test_path)
                    self.insert_logging_statements(self.test_class_path)
                    # Run the specific tests and capture output
                    output = self.compile_and_run_tests(list(tests_to_run))

                    if output is None:
                        print("Error occurred while running new/modified tests.")
                        return
                    method_calls = self.parse_output(output)

                    self.cleanup()
                    self.save_results_to_json(method_calls)

                # Now, check for changed methods and run the relevant test cases
                affected_methods = added_methods.union(modified_methods)
                for call, test_methods in existing_mapping.items():
                    if call in affected_methods:
                        method_calls[call] = test_methods

                if method_calls:
                    # Only run the test cases related to changed methods
                    print("Running tests for changed methods:", method_calls)
                    test_methods_to_run = [test_method for test_methods in method_calls.values() for test_method in test_methods]
                    self.compile_and_run_tests(test_methods_to_run)

            print("Analysis complete.")
            self.cleanup()
            return
        else:
            # If no existing mapping, create a new one by analyzing the code
            print("No existing mapping found. Creating a new one...")

            # If this is the first run, analyze the whole code
            print("Inserting logging statements into the class under test...")
            self.insert_logging_statements(self.class_under_test_path)

            print("Inserting logging statements into the Test...")
            self.insert_logging_statements(self.test_class_path)

            print("Compiling and running modified Java code and test class...")
            output = self.compile_and_run_tests()
            if output is None:
                return

            print("Parsing output to determine method calls...")
            method_calls = self.parse_output(output)

            self.cleanup()

            print("Analysis complete.")
            self.save_results_to_json(method_calls)

            return method_calls



if __name__ == "__main__":
    # Static analysis results: List of methods that were changed (for example)
    static_analysis_results = {
        "Modified_methods": {
            "BankAccount.deposit",
            "BankAccount.withdraw",
            "BankAccount.calculateInterest",
            "BankAccount.transfer",
            "BankAccount.sumPositiveBalances"
        },
        "Added_methods": {
            "BankAccount.getAccountSummary"
        },
        "Removed_methods": {
            "BankAccount.calculateInterestDivideByZero"
        },
        "Added_tests": {
            "BankAccountTest.testGetAccountSummary"
        },
        "Modified_tests": {
            "BankAccountTest.testTransferSuccess"
        },
        "Removed_tests": {
            "BankAccountTest.testCalculateInterestDivideByZero"
        }
    }
    class_under_test_path = "java/original/src/main/BankAccount.java"  # Path to the class that needs to be tested
    test_class_path = "java/original/test/BankAccountTest.java"  # Path to the JUnit test class
    project_path = "java/original"
    analyzer = DynamicJavaAnalyzer(class_under_test_path, test_class_path,project_path,static_analysis_results)
    results = analyzer.analyze()

    if results:
        analyzer.save_results_to_json(results)

    print("Analysis complete.")

