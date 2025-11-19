import sys 
import os
import json
import csv 
from pathlib import Path
from typing import List, Dict

def main() -> None:
    # Checks for valid command line arguments
    if len(sys.argv) != 2:
        print(f"Error: Usage: python3 sbom.py <directory_path>")
        sys.exit(1)

    directory = Path(sys.argv[1]).resolve()    # Converts command-line directory into absolute path

    # Checks whether directory exists
    if not directory.exists():
        print(f"Error: '{directory}' does not exist")
        sys.exit(1) 

    if not directory.is_dir():          
        print(f"Error: '{directory}' is not a directory")
        sys.exit(1)

    # Recursive search finding files within directory and all subdirectories 
    requirements_files = list(directory.rglob("requirements.txt"))      
    package_files = list(directory.rglob("package.json"))

    if not requirements_files and not package_files:
        print(f"Error: No requirements.txt or package.json files found in '{directory}'")
        sys.exit(1)

    dependencies = []       # List to store all discovered dependencies
    respositories = set()       # Set to store unique repositories (avoiding duplicates)

    # Parse all requirements.txt files and package.json files and collect dependencies 
    for file in requirements_files: 
        dependencies.extend(parse_requirements(file))
    for file in package_files: 
        dependencies.extend(parse_package(file))

    # Identify unique repositories by getting parent directory of each file with dependency
    for file in requirements_files + package_files:
        respositories.add(file.parent)
    
    print(f"Found {len(respositories)} repositories in {directory}")

    write_csv(dependencies, directory)
    write_json(dependencies, directory)

def write_csv(dependencies: List[Dict], directory: Path):   
    # Create full path for CSV file 
    path = os.path.join(directory, "sbom.csv")

    # Write dependencies to file with required columns
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "version", "type", "file_path"])
        for d in dependencies:
            writer.writerow([d["name"], d["version"], d["type"], d["file_path"]])
    
    print(f"Saved SBOM in CSV format to '{path}'")

def write_json(dependencies: List[Dict], directory: Path): 
    # Create full path for json file 
    path = os.path.join(directory, "sbom.json")

    data = {
        "dependencies": dependencies,
        "summary": {
            "total": len(dependencies),
            "pip": len([d for d in dependencies if d["type"] == "pip"]),
            "npm": len([d for d in dependencies if d["type"] == "npm"])
        }
    }
    
    with open(path, "w") as f:
        json.dump(data, f, indent = 2)
    
    print(f"Saved SBOM in JSON format to '{path}'")

def parse_requirements(file_path: Path) -> List[Dict]:
    dependencies = []

    # Read and parse file line by line 
    with file_path.open("r") as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines, comments, and options
            if not line or line.startswith("#") or line.startswith("-"):
                continue

            # Simple parsing: expect 'name==version'
            if "==" in line:
                name, version = line.split("==")
                name = name.strip()
                version = version.strip()
            
            # Add valid dependency to the list 
            if name:
                dependencies.append({
                    "name": name,
                    "version": version,
                    "type": "pip", 
                    "file_path": str(file_path.absolute())
                    })
    
    return dependencies

def parse_package(file_path: Path) -> List[Dict]:
    dependencies = []

    # Read file 
    with file_path.open("r") as file:
        content = file.read()
    
    # Parse json content from file 
    data = json.loads(content)

    # Extract dependencies 
    for section in ["dependencies", "devDependencies"]:
        for name, version in data[section].items():
            dependencies.append({
                "name": name,
                "version": version,
                "type": "npm", 
                "file_path": str(file_path.absolute())
            })
    
    return dependencies


if __name__ == "__main__":
    main()

