import os
import tempfile
import shutil
import git
import tkinter as tk
from tkinter import filedialog
from static_analysis.change_detector import ChangeDetector
from static_analysis.dependency_tracker import DependencyTracker

# Testing flag
TESTING = True



def find_src_folder(project_path):
    """
    Search for the `src` folder or the folder containing Java source files (.java) within the project directory.
    """
    for root, dirs, files in os.walk(project_path):
        # Check if the folder is explicitly named "src"
        if os.path.basename(root) == "src":
            return root
        
        # Check if the folder contains Java source files
        if any(file.endswith(".java") for file in files):
            return root  # Return the first folder containing Java files

    return None  # No `src` folder or Java files found


def select_folder(prompt="Select the project folder"):
    """
    Open a file explorer dialog to select a folder.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title=prompt)
    return folder_selected


def is_git_repo(path):
    """
    Check if the given path is a valid Git repository.
    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def extract_previous_commit(repo_path, temp_dir):
    """
    Extract the previous commit into a temporary directory using git archive.
    """
    repo = git.Repo(repo_path)

    # Ensure at least one previous commit exists
    if len(repo.head.commit.parents) == 0:
        raise ValueError("The repository does not have a previous commit to compare.")

    previous_commit = repo.head.commit.parents[0]

    # Use git archive to export the previous commit to the temporary directory
    archive_path = os.path.join(temp_dir, "archive.tar")
    repo.git.archive(previous_commit.hexsha, output=archive_path)
    shutil.unpack_archive(archive_path, temp_dir)

    print(f"Previous commit extracted to temporary directory: {temp_dir}")
    return temp_dir


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
        changes = detector.detect_changes(printer=True, showBodies=False)

    else:
        # Normal mode: Select Git-enabled project folder
        print("Select the Git-enabled project folder:")
        project_path = select_folder("Select the Git-enabled project folder")
        if not project_path:
            print("No folder selected. Exiting.")
            return

        if not is_git_repo(project_path):
            print(f"The selected folder '{project_path}' is not a valid Git repository. Exiting.")
            return

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
        dependencyTracker = DependencyTracker(find_src_folder(modified_path))
    else:
        dependencyTracker = DependencyTracker(find_src_folder(project_path))


    # Get all caller methods for the directly affected methods
    indirectly_affected_methods = dependencyTracker.provide_all_caller_methods(directly_affected_methods, printAST=True)

    print(f"\nIndirectly affected methods: {indirectly_affected_methods}\n")

    # Combine directly and indirectly affected methods
    all_possible_affected_methods = directly_affected_methods | indirectly_affected_methods
    print(f"All possible affected methods: {all_possible_affected_methods}\n")

        # changes_dynamic = {
    #         "directly_affected_methods": directly_affected_methods,
    #         "directly_affected_tests": directly_affected_tests,
    #         "removed_methods": removed_methods,
    #         "added_tests": added_tests,
    #         "removed_tests": removed_tests
    #     }


if __name__ == "__main__":
    main()
