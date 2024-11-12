from change_detector import ChangeDetector
from static_analysis.dependency_tracker import DependencyTracker


def main():
    """
    Perform an analysis of two different versions of the BankAccount class from two different Java projects.
    The tool will detect changes in the code and suggest all unit tests that should be rerun based on the changes.

    Is important to note that the original and modified folders are two separate Java projects, such that each one has its out folder.

    Before executing this script, in the "modified" project, you should:
    1) Make a change in the src/BankAccount class
    2) Open the project in your Java IDE and run the Main.java file to generate the BankAccount.class file
    3) Execute the jvm2json of the modified BankAccount.class and store the output in the out/json folder
    4) Run this main.py file
    """

    # ChangeDetector is a class that detects changes in Java code
    detector = ChangeDetector()
    [modified_methods, new_methods, removed_methods] = detector.detect_changes_in_java_code(printer=True, showBodies=False)

    directly_affected_methods = modified_methods + removed_methods
    print(f"Directly affected methods: {directly_affected_methods}")
    # print(f"Tests should be made for the following methods: {new_methods}")

    if not directly_affected_methods:
        print("No methods were directly affected. No need to run the dependency tracker.")
        return

    # DependencyTracker is a class can track all possible affected methods based in their dependencies of the directly affected methods
    dependencyTracker = DependencyTracker()
    all_possible_affected_methods = dependencyTracker.provide_all_affected_methods(directly_affected_methods)


    



if __name__ == "__main__":
    main()