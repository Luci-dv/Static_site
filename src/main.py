from textnode import TextNode, TextType
import os
import shutil
from block_to_html import markdown_to_html_node
from text_parser import extract_title
import sys

def copy_static(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    print(f"Creating directory: {dest_dir}")
    os.makedirs(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            copy_static(source_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")
    with open(from_path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    title_add = template.replace("{{ Title }}", title)
    final = title_add.replace("{{ Content }}", html)
    final = final.replace('href="/', f'href="{basepath}"')
    final = final.replace('src="/', f'src="{basepath}"')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(final)   
    print(f"File created at {dest_path}")

def generate_all_pages(content_dir, template_path, public_dir, basepath):
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_path = os.path.join(root, file)
                rel_path = os.path.relpath(markdown_path, content_dir)
                rel_path_html = os.path.splitext(rel_path)[0] + ".html"
                html_path = os.path.join(public_dir, rel_path_html)
                generate_page(markdown_path, template_path, html_path, basepath)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copy_static("static", "docs")
    generate_all_pages("content", "template.html", "docs", basepath)

# Call the main function when the script is run
if __name__ == "__main__":
    main()