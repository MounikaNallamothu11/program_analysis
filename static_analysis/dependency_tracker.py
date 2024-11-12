class DependencyTracker:

    def __init__(self, new_java_file_path: str = 'java/modified/src/BankAccount.java') -> None:
        self.new_java_code = self.read_java_file(new_java_file_path)
        

    def provide_all_affected_methods(self, affected_methods: list[str]) -> list[str]:
        """
        Track dependencies of the affected methods
        """
        pass


    def read_java_file(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            return file.read()