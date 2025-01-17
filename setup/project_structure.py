import os

def create_file(path):
    """Helper function to create an empty file."""
    with open(path, 'w') as file:
        pass

def create_academic_package_structure(base_dir):
    # Directories to create
    dirs = [
        os.path.join(base_dir, "core"),
        os.path.join(base_dir, "tests")
    ]
    
    # Files to create
    files = [
        os.path.join(base_dir, "__init__.py"),
        os.path.join(base_dir, "core/__init__.py"),
        os.path.join(base_dir, "core/class1.py"),
        os.path.join(base_dir, "core/class2.py"),
        os.path.join(base_dir, "services.py"),
        os.path.join(base_dir, "main.py"),
        os.path.join(base_dir, "tests/__init__.py"),
        os.path.join(base_dir, "tests/test_class1.py"),
        os.path.join(base_dir, "tests/test_class2.py"),
        os.path.join(base_dir, "requirements.txt"),
        os.path.join(base_dir, "README.md"),
        os.path.join(base_dir, "LICENSE"),
        os.path.join(base_dir, ".gitignore")
    ]
    
    # Create directories
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    
    # Create files
    for file_path in files:
        create_file(file_path)

if __name__ == "__main__":
    base_directory = input("Enter the base directory for your package: ").strip()
    create_academic_package_structure(base_directory)
    print(f"Structure created in {base_directory}.")