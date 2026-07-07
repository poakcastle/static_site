import blockmarkdown as bm
import os
from htmlnode import HTMLNode

def extract_title(markdown: str) -> str:
    blocks = bm.markdown_to_blocks(markdown)
    for block in blocks:
        if bm.block_to_block_type(block) == bm.BlockType.HEADING:
            words = block.split(" ", 1)
            if len(words[0]) == 1:
                return words[1].strip()
    raise Exception("Error: no h1 header was found in the markdown file")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, mode="r") as f:
        markdown = f.read()
    with open(template_path, mode="r") as f:
        template = f.read()
    html_node = bm.markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, mode="w") as f:
        f.write(full_html)

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    items = os.listdir(dir_path_content)
    for item in items:
        item_path = os.path.join(dir_path_content, item)
        dest_path = item_path.replace(dir_path_content, dest_dir_path, 1)
        if os.path.isfile(item_path):
            if item_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(item_path, template_path, dest_path)
        elif os.path.isdir(item_path):
            generate_page_recursive(item_path, template_path, dest_path)
    


    
    
    