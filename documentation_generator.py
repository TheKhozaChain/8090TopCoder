#!/usr/bin/env python3
import os
import re
import argparse
import json
from collections import OrderedDict
import shutil

def extract_title(markdown_content):
    """Extract title from markdown content, defaulting to filename if not found."""
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    return None

def extract_order(filename):
    """Extract order number from filename if it exists (e.g., 01_filename.md returns 1)."""
    # Special case: index.md should always be first
    if filename.lower() == 'index.md':
        return -1  # Ensures index.md is always first
        
    order_match = re.match(r'^(\d+)_', os.path.basename(filename))
    if order_match:
        return int(order_match.group(1))
    return 999  # Default to high number for files without order prefix

def collect_markdown_files(directory):
    """Collect all markdown files in a directory with their titles and order."""
    files = []
    
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            title = extract_title(content)
            if not title:
                # Use filename without extension and order prefix as title
                title = re.sub(r'^\d+_', '', os.path.splitext(filename)[0])
                title = title.replace('_', ' ').replace('-', ' ').capitalize()
                
                # Special case for index.md
                if filename.lower() == 'index.md':
                    title = "Overview"
            
            order = extract_order(filename)
            
            files.append({
                'filepath': filepath,
                'filename': filename,
                'html_filename': os.path.splitext(filename)[0] + '.html',
                'title': title,
                'order': order,
                'content': content
            })
    
    # Sort files by order
    files.sort(key=lambda x: x['order'])
    return files

def convert_markdown_to_html(markdown_content, title, navigation_html, next_prev_html, project_name=None):
    """Convert markdown to HTML with navigation."""
    # Escape content for JavaScript
    escaped_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    
    # Update the sidebar header to use project name if available
    sidebar_title = project_name if project_name else "Documentation"
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- Include Mermaid library -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <!-- Include Markdown-it for rendering markdown -->
    <script src="https://cdn.jsdelivr.net/npm/markdown-it@12/dist/markdown-it.min.js"></script>
    <style>
        :root {{
            --sidebar-width: 260px;
            --header-height: 60px;
            --primary-color: #0366d6;
            --background-color: #fff;
            --sidebar-background: #f8f9fa;
            --text-color: #333;
            --border-color: #e1e4e8;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            margin: 0;
            padding: 0;
            display: flex;
            min-height: 100vh;
        }}
        
        .sidebar {{
            width: var(--sidebar-width);
            background-color: var(--sidebar-background);
            border-right: 1px solid var(--border-color);
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            padding: 20px 0;
        }}
        
        .sidebar-header {{
            padding: 0 20px 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }}
        
        .sidebar-header h1 {{
            font-size: 1.5em;
            margin: 0;
        }}
        
        .nav-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .nav-item {{
            padding: 8px 20px;
        }}
        
        .nav-item.active {{
            background-color: rgba(3, 102, 214, 0.1);
            border-left: 3px solid var(--primary-color);
            padding-left: 17px;
            font-weight: 600;
        }}
        
        .nav-item a {{
            color: var(--text-color);
            text-decoration: none;
        }}
        
        .nav-item a:hover {{
            text-decoration: underline;
        }}
        
        .main-content {{
            flex: 1;
            margin-left: var(--sidebar-width);
            padding: 20px 40px;
            max-width: 800px;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.3em;
        }}
        
        p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        code {{
            font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            background-color: rgba(27, 31, 35, 0.05);
            border-radius: 3px;
        }}
        
        pre {{
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            margin: 0;
            font-size: 100%;
            word-break: normal;
            white-space: pre;
        }}
        
        .mermaid {{
            text-align: center;
        }}
        
        .pagination {{
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
        }}
        
        .pagination a {{
            display: inline-block;
            padding: 8px 16px;
            border: 1px solid var(--border-color);
            border-radius: 4px;
        }}
        
        .pagination a:hover {{
            background-color: rgba(3, 102, 214, 0.1);
        }}
        
        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
            }}
            
            .main-content {{
                margin-left: 0;
                padding: 20px;
            }}
            
            body {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <h1>{sidebar_title}</h1>
        </div>
        <nav>
            {navigation_html}
        </nav>
    </div>
    
    <div class="main-content">
        <div id="content"></div>
        
        {next_prev_html}
    </div>

    <script>
        // Initialize mermaid
        mermaid.initialize({{ startOnLoad: true }});
        
        // Initialize markdown-it
        const md = window.markdownit({{
            html: true,
            linkify: true,
            typographer: true
        }});
        
        // Custom renderer to handle internal links
        const defaultRender = md.renderer.rules.link_open || function(tokens, idx, options, env, self) {{
            return self.renderToken(tokens, idx, options);
        }};
        
        md.renderer.rules.link_open = function(tokens, idx, options, env, self) {{
            const href = tokens[idx].attrs.find(attr => attr[0] === 'href');
            
            if (href && href[1].endsWith('.md')) {{
                // Convert .md links to .html
                href[1] = href[1].replace(/\.md$/, '.html');
            }}
            
            return defaultRender(tokens, idx, options, env, self);
        }};
        
        // Markdown content directly embedded
        const markdownContent = `{escaped_content}`;
        
        // Render the markdown to HTML
        let htmlContent = md.render(markdownContent);
        
        // Replace mermaid code blocks with mermaid div
        htmlContent = htmlContent.replace(
            /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g, 
            '<div class="mermaid">$1</div>'
        );
        
        // Set the HTML content
        document.getElementById('content').innerHTML = htmlContent;
        
        // Initialize any mermaid diagrams
        mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        
        // Mark current page as active in navigation
        const currentPage = window.location.pathname.split('/').pop();
        const navLinks = document.querySelectorAll('.nav-item a');
        
        navLinks.forEach(link => {{
            const linkPage = link.getAttribute('href');
            if (linkPage === currentPage) {{
                link.parentElement.classList.add('active');
            }}
        }});
    </script>
</body>
</html>'''

    return html_content

def create_navigation_html(files, current_file):
    """Create HTML for the navigation sidebar."""
    navigation = ['<ul class="nav-list">']
    
    for file in files:
        active_class = 'class="active"' if file['filepath'] == current_file['filepath'] else ''
        navigation.append(f'<li class="nav-item" {active_class}><a href="{file["html_filename"]}">{file["title"]}</a></li>')
    
    navigation.append('</ul>')
    return '\n'.join(navigation)

def create_next_prev_html(files, current_file):
    """Create HTML for the next/previous navigation at the bottom of each page."""
    current_index = next((i for i, f in enumerate(files) if f['filepath'] == current_file['filepath']), -1)
    
    if current_index == -1:
        return ""
    
    prev_file = files[current_index - 1] if current_index > 0 else None
    next_file = files[current_index + 1] if current_index < len(files) - 1 else None
    
    prev_html = f'<a href="{prev_file["html_filename"]}">&laquo; {prev_file["title"]}</a>' if prev_file else '<span></span>'
    next_html = f'<a href="{next_file["html_filename"]}">{next_file["title"]} &raquo;</a>' if next_file else '<span></span>'
    
    return f'<div class="pagination">{prev_html}{next_html}</div>'

def process_internal_links(content, files):
    """Process internal links in markdown content to point to correct HTML files."""
    def replace_link(match):
        link = match.group(2)
        if link.endswith('.md'):
            base_name = os.path.basename(link)
            for file in files:
                if file['filename'] == base_name:
                    return f']({file["html_filename"]}'
        return f']({link}'
    
    pattern = r'(\]\()([^)]+\.md)(\))'
    return re.sub(pattern, replace_link, content)

def generate_documentation(input_dir, output_dir=None, project_name=None):
    """Generate a complete HTML documentation from markdown files."""
    if not os.path.isdir(input_dir):
        raise ValueError(f"Input directory {input_dir} does not exist")
    
    # If output directory is not specified, create a docs subdirectory
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'docs')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Collect all markdown files
    files = collect_markdown_files(input_dir)
    
    if not files:
        print(f"No markdown files found in {input_dir}")
        return
    
    # Process each file
    for current_file in files:
        # Process internal links
        processed_content = process_internal_links(current_file['content'], files)
        
        # Create navigation HTML
        navigation_html = create_navigation_html(files, current_file)
        
        # Create next/prev navigation
        next_prev_html = create_next_prev_html(files, current_file)
        
        # Convert to HTML
        html_content = convert_markdown_to_html(
            processed_content,
            project_name + " - " + current_file['title'] if project_name else current_file['title'],
            navigation_html,
            next_prev_html,
            project_name
        )
        
        # Write HTML file
        output_file = os.path.join(output_dir, current_file['html_filename'])
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created {output_file}")
    
    # Copy assets if they exist
    assets_dir = os.path.join(input_dir, 'assets')
    if os.path.isdir(assets_dir):
        output_assets_dir = os.path.join(output_dir, 'assets')
        if not os.path.isdir(output_assets_dir):
            os.makedirs(output_assets_dir, exist_ok=True)
        
        for asset in os.listdir(assets_dir):
            src = os.path.join(assets_dir, asset)
            dst = os.path.join(output_assets_dir, asset)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"Copied asset {asset}")
    
    print(f"\nDocumentation generated successfully in {output_dir}")
    
    # Find the first file to open (preferably index.html)
    first_file = next((f['html_filename'] for f in files if f['filename'].lower() == 'index.md'), files[0]['html_filename'])
    
    print(f"Open {os.path.join(output_dir, first_file)} to start browsing")
    
    return output_dir, first_file

def main():
    parser = argparse.ArgumentParser(description='Generate HTML documentation from markdown files')
    parser.add_argument('input_dir', help='Directory containing markdown files')
    parser.add_argument('-o', '--output', help='Output directory for HTML files (default: input_dir/docs)')
    parser.add_argument('-n', '--name', help='Project name to include in page titles')
    
    args = parser.parse_args()
    
    try:
        output_dir, first_file = generate_documentation(args.input_dir, args.output, args.name)
        
        # Try to open the first file in the browser
        first_file_path = os.path.join(output_dir, first_file)
        try:
            import webbrowser
            webbrowser.open('file://' + os.path.abspath(first_file_path))
        except:
            pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 