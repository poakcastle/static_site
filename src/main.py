import os
import shutil
from copystatic import copy_dir_content
from gencontent import generate_page_recursive

def main():
    public = "public"
    static = "static"
    content = "content"
    template = "template.html"
    if os.path.exists(public):
        shutil.rmtree(public)
    copy_dir_content(static)
    print("Transfer complete!")
    generate_page_recursive(content, template, public)

main()