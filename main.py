from static_analysis.change_detector import ChangeDetector
from static_analysis.dependency_tracker import DependencyTracker


def main():
    """
    Perform an analysis of two different versions of the BankAccount class from two different Java projects.
    The tool will detect changes in the code and suggest all unit tests that should be rerun based on the changes.

    It is important to note that the original and modified folders are two separate Java projects, such that each one has its own folder.

    Before executing this script, in the "modified" project, you should:
    1) Make a change in the src/BankAccount class
    2) Open the project in your Java IDE and run the Main.java file to generate the BankAccount.class file
    3) Execute the jvm2json of the modified BankAccount.class and store the output in the out/json folder
    4) Run this main.py file
    """

    # ChangeDetector is a class that detects changes in Java code
    detector = ChangeDetector()
    changes = detector.detect_changes(printer=True, showBodies=False)

    modified_methods = changes["modified_methods"]
    added_methods = changes["added_methods"]
    removed_methods = changes["removed_methods"]
    modified_tests = changes["modified_tests"]
    added_tests = changes["added_tests"]
    removed_tests = changes["removed_tests"]


    # Combine directly affected methods (modified and removed)
    directly_affected_methods = modified_methods | removed_methods

    # Combine directly affected tests (modified and removed)
    directly_affected_tests = modified_tests | removed_tests


    if directly_affected_methods:
        print(f"\nDirectly affected methods: {directly_affected_methods}")
    # else:
    #     print("\nNo methods were directly affected, thus no tests should be rerun.")

    if directly_affected_tests:
        print(f"\nDirectly affected tests: {directly_affected_tests}")
        
    if added_methods:
        print(f"\nNew tests should be made for the following methods: {added_methods}")

    if added_tests:
        print(f"\nNew tests were added but still haven't run: {added_tests}")
        

    # DependencyTracker is a class that creates an AST of a Java file to track all caller methods of a given list of methods
    dependencyTracker = DependencyTracker()

    # Get all caller methods for the directly affected methods
    indirectly_affected_methods = dependencyTracker.provide_all_caller_methods(directly_affected_methods)

    print(f"\nIndirectly affected methods: {indirectly_affected_methods}\n")

    # Combine directly and indirectly affected methods
    all_possible_affected_methods = directly_affected_methods | indirectly_affected_methods
    print(f"All possible affected methods: {all_possible_affected_methods}\n")


if __name__ == "__main__":
    main()
