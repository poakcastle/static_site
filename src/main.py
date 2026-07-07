import os
import shutil
import sys
from copystatic import copy_dir_content
from gencontent import generate_page_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    destination = "docs"
    static = "static"
    content = "content"
    template = "template.html"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    copy_dir_content(static, destination)
    print("Transfer complete!")
    generate_page_recursive(content, template, destination, basepath)

main()