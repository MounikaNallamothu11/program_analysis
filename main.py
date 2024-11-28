import os
import tempfile
import json
from static_analysis.change_detector import ChangeDetector
from static_analysis.dependency_tracker import DependencyTracker
from dynamic_analysis.DynamicJavaAnalyzer import DynamicJavaAnalyzer
from utils import find_path_to_folder, select_folder, is_git_repo, extract_previous_commit, save_last_project_path, get_last_project_path

# User flags
TESTING = False
PRINT_AST = True
SHOW_METHOD_BODIES = False
USE_LAST_PROJECT_PATH = True


def main():
    """
    Analyze a Java project to detect changes and affected tests.
    """

    if TESTING:
        print("\nTESTING mode enabled: Using java/original and java/modified folders for analysis.\n")

        # Paths for original and modified projects in TESTING mode
        original_path = "java/original"
        modified_path = "java/modified"

        if not os.path.isdir(original_path) or not os.path.isdir(modified_path):
            print(f"TESTING paths '{original_path}' or '{modified_path}' are invalid. Exiting.")
            return

        # Perform analysis using ChangeDetector
        detector = ChangeDetector(original_path, modified_path)
        changes = detector.detect_changes(printer=True, showBodies=SHOW_METHOD_BODIES)

    else:
        # Retrieve project path
        project_path = None
        if USE_LAST_PROJECT_PATH:
            project_path = get_last_project_path()
            if project_path and os.path.isdir(project_path):
                print(f"Using last project path: {project_path}")
            else:
                print("Last project path is invalid or missing. Please select a folder.")
                project_path = None

        if not project_path:
            # Prompt the user to select a folder
            print("Select the Git-enabled project folder:")
            project_path = select_folder("Select the Git-enabled project folder")
            if not project_path:
                print("No folder selected. Exiting.")
                return

            if not is_git_repo(project_path):
                print(f"The selected folder '{project_path}' is not a valid Git repository. Exiting.")
                return

            # Save the selected project path
            save_last_project_path(project_path)

        print(f"Project folder selected: {project_path}\n")

        # Prepare a temporary folder for the previous commit
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                print("Extracting the previous commit into a temporary folder...")
                extract_previous_commit(project_path, temp_dir)
                print("Previous commit extracted successfully.\n")

                # Perform analysis using ChangeDetector
                detector = ChangeDetector(temp_dir, project_path)
                changes = detector.detect_changes(printer=True, showBodies=False)

            except ValueError as e:
                print(f"Error: {e}")
                return
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return

    # Handle and display the detected changes
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

    if directly_affected_tests:
        print(f"\nDirectly affected tests: {directly_affected_tests}")

    if added_methods:
        print(f"\nNew tests should be made for the following methods: {added_methods}")

    if added_tests:
        print(f"\nNew tests were added but still haven't run: {added_tests}")

    if TESTING:
        # DependencyTracker is a class that creates an AST of a Java file to track all caller methods of a given list of methods
        dependencyTracker = DependencyTracker(find_path_to_folder(modified_path, "src"))
    else:
        dependencyTracker = DependencyTracker(find_path_to_folder(project_path, "src"))

    # Get all caller methods for the directly affected methods
    indirectly_affected_methods = dependencyTracker.provide_all_caller_methods(directly_affected_methods, printAST=PRINT_AST)

    print(f"\nIndirectly affected methods: {indirectly_affected_methods}\n")

    # Combine directly and indirectly affected methods
    all_possible_affected_methods = directly_affected_methods | indirectly_affected_methods
    print(f"All possible affected methods: {all_possible_affected_methods}\n")

    # Dynamic analysis
    changes_dynamic = {
        "directly_affected_methods": directly_affected_methods,
        "removed_methods": removed_methods,
        "added_methods": added_methods,
        "added_tests": added_tests,
        "modified_tests": modified_tests,
        "removed_tests": removed_tests,
    }
    if TESTING:
        dynamicAnalyzer = DynamicJavaAnalyzer(modified_path, changes_dynamic)
    else:
        dynamicAnalyzer = DynamicJavaAnalyzer(project_path, changes_dynamic)

    dynamicAnalyzer.analyze()


if __name__ == "__main__":
    main()
