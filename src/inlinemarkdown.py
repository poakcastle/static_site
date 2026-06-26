from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
        elif node.text is not None:
            split_strings = node.text.split(delimiter)
            if len(split_strings) % 2 == 0:
                raise Exception(f"Error: invalid markdown synthax, expected odd number of strings after splitting")
            for i in range(len(split_strings)):
                if len(split_strings[i]) == 0:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_strings[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(split_strings[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[(str)]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> list[(str)]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
            continue
        elif node.text is not None:
            links = extract_markdown_links(node.text)
            raw_string = node.text
            if len(links) == 0:
                new_nodes.append(node)
                continue
            for link in links:
                split_strings = raw_string.split(f"[{link[0]}]({link[1]})", maxsplit=1)
                if len(split_strings) != 2:
                    raise ValueError("Error: invalid markdown synthax")
                if len(split_strings[0]) > 0:
                    new_nodes.append(TextNode(split_strings[0], TextType.PLAIN))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                raw_string = split_strings[1]
            if len(raw_string) > 0:
                new_nodes.append(TextNode(raw_string, TextType.PLAIN))
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
            continue
        elif node.text is not None:
            images = extract_markdown_images(node.text)
            raw_string = node.text
            if len(images) == 0:
                new_nodes.append(node)
                continue
            for image in images:
                split_strings = raw_string.split(f"![{image[0]}]({image[1]})", maxsplit=1)
                if len(split_strings) != 2:
                    raise ValueError("Error: invalid markdown synthax")
                if len(split_strings[0]) > 0:
                    new_nodes.append(TextNode(split_strings[0], TextType.PLAIN))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                raw_string = split_strings[1]
            if len(raw_string) > 0:
                new_nodes.append(TextNode(raw_string, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes