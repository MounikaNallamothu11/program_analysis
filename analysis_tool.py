from dynamic_analysis import detect_changes

if __name__ == "__main__":
    # Assuming the source code is located in 'src/' directory
    source_directory = 'src/'
    snapshot_file = 'code_snapshot.json'
    
    # Run change detection
    detect_changes(source_directory, snapshot_file)

