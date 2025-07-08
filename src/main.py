import os
import pathlib
import re
import shutil
import sys
from markdown.parse_block_markdown import extract_markdown, extract_title
from node.blocknode import BlockType
from node.markdownToHtmlNode import markdown_to_html_node


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    dest_path = "docs"
    copy_folder("static", dest_path)
    generate_page_recursive("content", "template.html", dest_path, basepath)


def copy_folder(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_folder(s, d)
        else:
            shutil.copy(s, d)


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        absolute_path = os.path.join(dir_path_content, item)
        is_file = os.path.isfile(absolute_path)
        if is_file:
            new_file = pathlib.Path(absolute_path).stem + ".html"
            dest_path = os.path.join(dest_dir_path, new_file)
            generate_page(absolute_path, template_path, dest_path, basepath)
        else:
            new_absolute_path = os.path.join(dir_path_content, item)
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_page_recursive(
                new_absolute_path, template_path, new_dest_dir_path, basepath
            )


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path} using template {template_path}"
    )
    md = ""
    with open(from_path, "r") as f:
        md = f.read()
    template = ""
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


if __name__ == "__main__":
    main()
