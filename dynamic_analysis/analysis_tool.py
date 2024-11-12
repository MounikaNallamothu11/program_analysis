import json
import re

class DynamicAnalysis:
    def __init__(self, class_json_path):
        """
        Initialize with the path to the class JSON file (BankAccount.json)
        """
        self.class_json_path = class_json_path
        self.test_coverage = {}
        self.class_data = self.load_json(self.class_json_path)

    def load_json(self, json_path):
        with open(json_path, 'r') as file:
            return json.load(file)

    def load_test_file(self, test_file_path):
        with open(test_file_path, 'r') as file:
            return file.read()

    def trace_test_execution(self, test_name, executed_methods):
        if test_name not in self.test_coverage:
            self.test_coverage[test_name] = []

        # Add the methods covered by this test (avoid duplicates)
        for method in executed_methods:
            if method not in self.test_coverage[test_name]:
                self.test_coverage[test_name].append(method)
        print(f"Test '{test_name}' exercises methods: {executed_methods}")

    def get_method_coverage(self):
        return self.test_coverage

    def analyze_method(self, method):
        covered_methods = []
        # Extract methods from the method data
        for m in self.class_data['methods']:
            if m['name'] == method:
                for line in m['code']['lines']:
                    covered_methods.append({
                        "method": m['name'],
                        "line": line['line']
                    })
        return covered_methods

    def run_analysis(self, test_name, executed_methods):
        print(f"Running analysis for test '{test_name}'...")
        self.trace_test_execution(test_name, executed_methods)

    def print_test_coverage(self):
        coverage = self.get_method_coverage()
        if not coverage:
            print("No test coverage data available.")
        for test, methods in coverage.items():
            print(f"Test: {test}")
            for method in methods:
                print(f"  Method: {method}")

    def parse_test_methods(self, test_file_path):
        test_file_content = self.load_test_file(test_file_path)

        # Regular expression to find method names (assuming they are in the format "public void testXYZ()")
        method_pattern = re.compile(r'\bpublic\s+void\s+test([A-Za-z0-9_]+)\s*\(')
        return method_pattern.findall(test_file_content)

    def parse_method_calls(self, test_file_path):
        test_file_content = self.load_test_file(test_file_path)

        # Find all test methods using regex
        method_calls_pattern = re.compile(r'\bpublic\s+void\s+test([A-Za-z0-9_]+)\s*\([^)]*\)\s*\{([^}]*)\}')

        # This will store the methods called inside each test case
        method_calls = {}

        # Loop through each test method found in the file
        for match in method_calls_pattern.finditer(test_file_content):
            test_method = match.group(1)
            method_body = match.group(2)

            # Now, find method calls inside the body of the test case
            call_pattern = re.compile(r'\b[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)?\s*\([^\)]*\)\s*;')

            # Find method calls in the test method body
            calls_in_method = call_pattern.findall(method_body)

            # Extract the method names from the calls
            method_calls[test_method] = []
            for call in calls_in_method:
                # For example, 'account.deposit(50);' => 'deposit'
                method_name = call.split('(')[0].split('.')[-1]
                # Filter out irrelevant names like 'BankAccount' or 'assertEquals'
                if method_name not in ['BankAccount', 'assertEquals']:
                    method_calls[test_method].append(method_name)

        return method_calls

    def store_dynamic_analysis(self, output_file):
        with open(output_file, 'w') as outfile:
            json.dump(self.test_coverage, outfile, indent=4)
        print(f"Dynamic analysis data stored in {output_file}")


# Usage
if __name__ == "__main__":

    version = "Original"  # Original or Modified

    if version == "Original":
        # Paths to JSON and Test files
        bank_account_json_path = 'java/original/out/json/BankAccount.json'  # Path to your BankAccount.json
        test_file_path = 'java/original/test/BankAccountTest.java'  # Path to your BankAccountTest.java file
    else:
        # Paths to JSON and Test files
        bank_account_json_path = 'java/modified/out/json/BankAccount.json'  # Path to your BankAccount.json
        test_file_path = 'java/modified/test/BankAccountTest.java'  # Path to your BankAccountTest.java file

    # Create DynamicAnalysis instance
    analyzer = DynamicAnalysis(bank_account_json_path)

    # Parse the test file for method calls (e.g., deposit(), transfer(), getBalance())
    method_calls = analyzer.parse_method_calls(test_file_path)

    # For each test method, simulate that it exercises specific methods in BankAccount
    for test_method, executed_methods in method_calls.items():
        analyzer.run_analysis(test_method, executed_methods)

    # Store the dynamic analysis results to a JSON file
    analyzer.store_dynamic_analysis('dynamic_analysis/dynamic_analysis_output.json')
    # Print the test coverage mapping
    analyzer.print_test_coverage()
