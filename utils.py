import os
import shutil
import git
import tkinter as tk
from tkinter import filedialog


def find_path_to_folder(project_path, folder_name):
    """
    Search for the `src` folder or the folder containing Java source files (.java) within the project directory.
    """
    for root, dirs, files in os.walk(project_path):
        # Check if the folder is explicitly named "src"
        if os.path.basename(root) == folder_name:
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