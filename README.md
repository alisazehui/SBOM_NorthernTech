# SBOM Tool

A command-line tool for generating Software Bill of Materials (SBOM) from source code repositories. This tool scans directories for Python and Node.js projects and extracts dependency information to create software inventories.


## Features

- 🔍 **Automated Discovery**: Recursively scans directories for dependency files
- 📦 **Multi-language Support**: Supports both Python (`requirements.txt`) and Node.js (`package.json`) projects
- 📊 **Dual Output**: Generates CSV and JSON format SBOM files
- 🎯 **Repository Detection**: Identifies and counts unique code repositories
- 📋 **Comprehensive Data**: Extracts package names, versions, types, and source file paths


## How to use

```bash
python3 sbom.py <directory_path>
```

## Known Issues / Limitations 
- Only supports Python requirements in the form `name==version`. Other specifiers like `>=`, `<=`, `~=`, or environment markers are currently ignored.
- Only writes to CSV and JSON in the specified root directory — no custom output path.
- Parsing performance may reduce with large directory structures or huge files.



## Future Ideas / Possible Improvements 
- Support more complex Python requirement formats 
- Parallel scanning for large directory sets.
- Build a UI dashboard for exploring SBOMs interactively.
- Support additional ecosystems: Maven, Gradle, Go, Rust, Ruby, PHP, etc.


