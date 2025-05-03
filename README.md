# Documentation Generator System

This system generates interactive HTML documentation from markdown files, with a focus on code repositories and API documentation. It supports mermaid diagrams, code highlighting, and proper navigation between pages.

## Features

- **Automatic Navigation**: Sidebar with links to all documentation pages
- **Mermaid Diagram Support**: Renders mermaid diagrams in the documentation
- **Intelligent Page Ordering**: Prioritizes index.md as the main entry point
- **Next/Previous Navigation**: Easy navigation between pages with next/previous buttons
- **Responsive Design**: Works on mobile and desktop devices
- **Code Highlighting**: Properly formats and highlights code blocks
- **Automatic Link Processing**: Converts `.md` links to `.html` automatically
- **Project Title Integration**: Uses the project name in titles and navigation

## Components

This system includes three main components:

1. **markdown_to_html.py**: Simple converter for individual markdown files to HTML
2. **documentation_generator.py**: Complete documentation system with navigation and linking
3. **Integration with pocketflow/main.py**: Automatic documentation generation for repositories

## Usage

### Basic HTML Generation

Convert individual markdown files to HTML:

```bash
python3 markdown_to_html.py path/to/file.md
```

### Interactive Documentation Generation

Generate complete documentation with navigation from a directory of markdown files:

```bash
python3 documentation_generator.py input_directory -n "Project Name"
```

### GitHub Repository Analysis

Analyze a GitHub repository and generate documentation:

```bash
python3 pocketflow/main.py --repo https://github.com/username/repo --interactive-docs
```

For better performance with GitHub repositories, use a personal access token:

```bash
python3 pocketflow/main.py --repo https://github.com/username/repo --interactive-docs --token YOUR_GITHUB_TOKEN
```

## Configuration Options

The documentation generator supports several options:

- **Project Name**: Displayed in the sidebar and page titles
- **Output Directory**: Custom location for generated files
- **File Selection**: Include/exclude specific file patterns
- **HTML Generation**: Simple HTML or interactive documentation

## Recent Improvements

- Fixed the documentation to start with the main overview page (index.md)
- Added project name display in the sidebar header
- Improved title extraction and formatting
- Enhanced navigation with proper ordering and highlighting
- Better project name detection from repository URLs
- Added support for copying static assets

## Examples

The documentation generator has been successfully tested on:

- Token Metrics AI API repository
- Other open-source projects with various documentation structures

## Requirements

- Python 3.6+
- Web browser with JavaScript support (for viewing documentation)
- Internet connection (for mermaid.js and markdown-it libraries) 