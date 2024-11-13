import os
from subprocess import Popen, PIPE
import re
import shutil
import json

class DynamicJavaAnalyzer:
    def __init__(self, class_under_test_path, test_class_path, project_path):
        self.class_under_test_path = os.path.abspath(f"{class_under_test_path}")  # The class to be tested
        self.test_class_path = os.path.abspath(f"{test_class_path}")  # The JUnit test class path
        self.project_path = project_path
        # Backup file path for restoring the original class after modifications
        self.backup_class_path = os.path.abspath(f"{class_under_test_path}.bak")
        self.backup_test_path = os.path.abspath(f"{test_class_path}.bak")
        self.class_name = os.path.basename(self.class_under_test_path).split('.')[0]

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
                modified_code.append(f'        System.out.println("CALL {method_name}");\n')  # Insert print inside method body
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

    def compile_and_run_tests(self):
        """
        Compiles and runs the modified class under test, along with the JUnit test class, using Maven.
        """       
        # Navigate to the Maven project directory
        os.chdir(self.project_path)

        args = ['mvn','clean', 'test']
        process = Popen(args,stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = process.communicate()

        # Check for compilation or test run errors
        if process.returncode != 0:
            print("Maven build and test failed with errors:")
            print(stderr.decode())
            return None

        # Return the stdout (which contains the test results) for further analysis
        print(stdout.decode())
        return stdout.decode()
    
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
    
    def save_results_to_json(self, results):
        """
        Saves the analysis results to a JSON file named 'dynamic_analysis_output.json'.
        """
        formatted_results = [
            {"test_method": test_method, "calls": calls}
            for test_method, calls in results.items()
        ]

        output_file = 'dynamic_analysis_output.json'
        with open(output_file, 'w') as f:
            json.dump(formatted_results, f, indent=4)
        
        print(f"Results saved to {output_file}")

    def analyze(self):
        """
        Full analysis pipeline: backup, instrument, compile, run, and analyze output, then restore original file.
        """
        print("Backing up the original class file...")
        self.backup_original_file(self.class_under_test_path,self.backup_class_path)
        
        print("Backing up the original test file...")
        self.backup_original_file(self.test_class_path,self.backup_test_path)

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

        print("Restoring the original class file...")
        self.restore_original_file(self.class_under_test_path,self.backup_class_path)
        
        print("Restoring the original test file...")
        self.restore_original_file(self.test_class_path,self.backup_test_path)

        print("Deleting class backup file...")
        self.delete_backup(self.backup_class_path)

        print("Deleting test backup file...")
        self.delete_backup(self.backup_test_path)

        print("Analysis complete.")
        return method_calls
    



if __name__ == "__main__":
    # Usage example:
    class_under_test_path = "java/original/src/main/BankAccount.java"  # Path to the class that needs to be tested
    test_class_path = "java/original/test/BankAccountTest.java"  # Path to the JUnit test class
    project_path = "java/original"
    analyzer = DynamicJavaAnalyzer(class_under_test_path, test_class_path,project_path)
    results = analyzer.analyze()

    if results:
            analyzer.save_results_to_json(results)

    print("Analysis complete.")

