import os
import re
import hashlib
import json

execution_paths = {}

def generate_function_hash(function_body: str) -> str:
    """Generate a hash for a given function body."""
    return hashlib.md5(function_body.encode('utf-8')).hexdigest()

def parse_code_and_create_snapshot(directory: str) -> dict:
    """Parse code in the directory and create a snapshot."""
    snapshot = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):  # Adjust this for Java or other languages
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    # Simplified way to extract methods (adjust the regex as needed)
                    methods = re.findall(r'def\s+(\w+)\(.*?\):\n(.*?)\n\n', content, re.DOTALL)
                    
                    for method_name, method_body in methods:
                        method_hash = generate_function_hash(method_body)
                        snapshot[method_name] = method_hash
    return snapshot

def save_snapshot(snapshot: dict, snapshot_file: str):
    """Save snapshot to a file."""
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f)

def load_snapshot(snapshot_file: str) -> dict:
    """Load snapshot from a file."""
    if not os.path.exists(snapshot_file):
        return {}
    with open(snapshot_file, 'r') as f:
        return json.load(f)

def compare_snapshots(old_snapshot: dict, new_snapshot: dict):
    """Compare old and new snapshots to detect changes."""
    added = []
    removed = []
    modified = []

    for method_name, new_hash in new_snapshot.items():
        old_hash = old_snapshot.get(method_name)
        if not old_hash:
            added.append(method_name)
        elif old_hash != new_hash:
            modified.append(method_name)
    
    for method_name in old_snapshot:
        if method_name not in new_snapshot:
            removed.append(method_name)
    
    return added, removed, modified

def detect_changes(directory: str, snapshot_file: str):
    """Detect changes between current code and the saved snapshot."""
    old_snapshot = load_snapshot(snapshot_file)
    new_snapshot = parse_code_and_create_snapshot(directory)
    added, removed, modified = compare_snapshots(old_snapshot, new_snapshot)

    # Save the updated snapshot
    save_snapshot(new_snapshot, snapshot_file)
    
    print(f"Added Methods: {added}")
    print(f"Removed Methods: {removed}")
    print(f"Modified Methods: {modified}")

