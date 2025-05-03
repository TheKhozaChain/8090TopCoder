#!/usr/bin/env python3
import os
import argparse
import html
import re

def convert_markdown_to_html(markdown_file, output_file=None):
    """Convert a markdown file to HTML with mermaid support."""
    
    # If output file not specified, use same name with .html extension
    if output_file is None:
        output_file = os.path.splitext(markdown_file)[0] + '.html'
    
    # Read the markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Escape the content for embedding in JavaScript
    escaped_content = markdown_content.replace('`', '\\`').replace('${', '\\${')
    
    # Create the HTML with embedded content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Viewer with Mermaid</title>
    <!-- Include Mermaid library -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <!-- Include Markdown-it for rendering markdown -->
    <script src="https://cdn.jsdelivr.net/npm/markdown-it@12/dist/markdown-it.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}
        a {{
            color: #0366d6;
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
    </style>
</head>
<body>
    <div id="content"></div>

    <script>
        // Initialize mermaid
        mermaid.initialize({{ startOnLoad: true }});
        
        // Initialize markdown-it
        const md = window.markdownit();
        
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
    </script>
</body>
</html>'''

    # Write the HTML to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Converted {markdown_file} to HTML file: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML with Mermaid support')
    parser.add_argument('markdown_file', help='Path to the Markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file path (default: same name with .html extension)')
    
    args = parser.parse_args()
    
    convert_markdown_to_html(args.markdown_file, args.output)

if __name__ == '__main__':
    main() 