from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str | None, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type.value == "text":
        return LeafNode(None, text_node.text)
    elif text_node.text_type.value == "bold":
        return LeafNode("b", text_node.text)
    elif text_node.text_type.value == "italic":
        return LeafNode("i", text_node.text)
    elif text_node.text_type.value == "code":
        return LeafNode("code", text_node.text)
    elif text_node.text_type.value == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type.value == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Error: {text_node.text_type} is not supported for conversion to HTMLNode")
    
        
        
    