from change_detector import ChangeDetector

detector = ChangeDetector()
[modified_methods, new_methods, removed_methods] = detector.detect_changes_in_java_code(printer=True, showBodies=True)

affected_methods = modified_methods + removed_methods

print(f"Affected methods: {affected_methods}")







# print(f"Tests should be made for the following methods: {new_methods}")