import os
import git
import time
import json
import shutil
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "config.json"


import os

def load_config(config_file="config.json"):
    """
    Load configuration data from a JSON file.

    Args:
        config_file (str): Path to the configuration file (default: "config.json").

    Returns:
        dict: Configuration data or an empty dictionary if the file does not exist.
    """
    if os.path.isfile(config_file):
        with open(config_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Error: Configuration file is corrupted. Loading default settings.")
    return {}


def save_config(data, config_file="config.json"):
    """
    Save configuration data to a JSON file.

    Args:
        data (dict): The configuration data to save.
        config_file (str): Path to the configuration file (default: "config.json").
    """
    with open(config_file, "w") as f:
        json.dump(data, f, indent=4)


def find_path_to_folder(project_path, folder_name):
    """
    Search for a specific folder within the project directory, excluding folders inside "out".
    
    Args:
        project_path (str): The base path to start searching.
        folder_name (str): The name of the folder to find.
        
    Returns:
        str: The path to the specified folder or None if not found.
    """
    # Normalize folder_name to avoid issues with leading/trailing slashes
    folder_name = folder_name.strip(os.sep)
    
    for root, dirs, files in os.walk(project_path):
        # Normalize root for comparison
        normalized_root = os.path.normpath(root)
        
        # Skip folders inside the "out" folder
        if "out" in normalized_root.split(os.sep):
            continue

        # Match exact folder name
        if os.path.basename(normalized_root) == folder_name:
            return normalized_root

    return None  # No matching folder found



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


def get_last_project_path():
    """Retrieve the last project path from the config file."""
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config.get("last_project_path")
    except json.JSONDecodeError:
        print(f"Error reading {CONFIG_FILE}. It may be corrupted.")
        return None


def save_last_project_path(path):
    """Save the last project path to the config file, preserving other fields."""
    try:
        # Load existing config if the file exists
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        else:
            config = {}

        # Update the last project path
        config["last_project_path"] = path

        # Save updated config back to the file
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    except Exception as e:
        print(f"Error saving to {CONFIG_FILE}: {e}")


def measure_time(label, func, *args, **kwargs):
    """
    Measure the execution time of a function.

    Args:
        label (str): The name of the process being measured.
        func (callable): The function to execute.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        tuple: (result, elapsed_time_ms)
            result: The return value of the function.
            elapsed_time_ms: The time taken to execute in milliseconds.
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_time_ms = (time.perf_counter() - start_time) * 1000
    return result, elapsed_time_ms


def load_maven_path(config_file="config.json"):
    """
    Loads the Maven path from the specified configuration file.

    Args:
        config_file (str): Path to the configuration file (default: "config.json").

    Returns:
        str: The Maven path if successfully loaded, otherwise None.
    """
    if not os.path.isfile(config_file):
        print(f"Configuration file '{config_file}' not found.")
        return None

    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        
        maven_path = config.get("maven_path", "").strip()
        if not maven_path:
            print("Maven path is missing or empty in the configuration file.")
            return None
        
        return maven_path

    except json.JSONDecodeError as e:
        print(f"Error parsing the configuration file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None