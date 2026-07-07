from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode
from inlinemarkdown import text_to_textnodes
from textnode import text_node_to_html_node
import textwrap

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        block = block.strip()
        if len(block) > 0:
            blocks.append(block)
    return blocks

def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        words = block.split(" ", maxsplit=1)
        if 1 <= len(words[0]) <= 6:
            for letter in words[0]:
                if letter != "#":
                    return BlockType.PARAGRAPH
            return BlockType.HEADING
        return BlockType.PARAGRAPH
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not str(line).startswith(">"):
               return BlockType.PARAGRAPH 
        return BlockType.QUOTE
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if not str(line).startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    elif block.startswith("1. "):
        lines = block.split("\n")
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED
    else:
        return BlockType.PARAGRAPH

def block_to_leaf_nodes(block: str) -> list[HTMLNode]:
    leaf_nodes = []
    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

def paragraph_to_block_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_block = ""
    for line in lines:
        new_block += f"{line.strip()} "
    children = block_to_leaf_nodes(new_block.strip())
    return ParentNode("p", children)

def heading_to_block_node(block: str) -> HTMLNode:
    words = block.split(" ", maxsplit=1)
    children = block_to_leaf_nodes(words[1])
    return ParentNode(f"h{len(words[0])}", children)

def quote_to_block_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        line = line.lstrip(">").strip()
        new_lines.append(line)
    new_block = ""
    for line in new_lines:
        new_block += f"{line} "
    children = block_to_leaf_nodes(new_block.strip())
    return ParentNode("blockquote", children)

def unordered_to_block_node(block: str) -> HTMLNode:
    unordered = []
    lines = block.split("\n")
    for line in lines:
        words = line.split("- ", maxsplit=1)
        children = block_to_leaf_nodes(words[1])
        unordered.append(ParentNode("li", children))
    return ParentNode("ul", unordered)

def ordered_to_block_node(block: str) -> HTMLNode:
    ordered = []
    lines = block.split("\n")
    for line in lines:
        words = line.split(". ", maxsplit=1)
        children = block_to_leaf_nodes(words[1])
        ordered.append(ParentNode("li", children))
    return ParentNode("ol", ordered)

def code_to_block_node(block: str) -> HTMLNode:
    new_block = block.strip("`")
    new_block = new_block.lstrip("\n")
    return ParentNode("pre", [LeafNode("code", textwrap.dedent(new_block))]) 

def block_to_block_node(block: str, block_type: BlockType) -> HTMLNode:
    if block_type.value == "paragraph":
        return paragraph_to_block_node(block)
    elif block_type.value == "heading":
        return heading_to_block_node(block)
    elif block_type.value == "quote":
        return quote_to_block_node(block)
    elif block_type.value == "unordered_list":
        return unordered_to_block_node(block)
    elif block_type.value == "ordered_list":
        return ordered_to_block_node(block)
    elif block_type.value == "code":
        return code_to_block_node(block)
    else:
        raise Exception("Error: invalid BlockType")    

def markdown_to_html_node(markdown: str) -> HTMLNode:
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        block_nodes.append(block_to_block_node(block, block_type))
    return ParentNode("div", block_nodes)
