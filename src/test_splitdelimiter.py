from inlinemarkdown import split_nodes_delimiter, text_to_textnodes
from textnode import TextNode, TextType
import unittest

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_bold(self):
        old_nodes = [TextNode("this is **bold** text", TextType.PLAIN)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "**", 
                TextType.BOLD
            ),
            [TextNode("this is ", TextType.PLAIN), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.PLAIN)]
        )

    def test_italic(self):
        old_nodes = [TextNode("this is _italic_ text", TextType.PLAIN)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "_", 
                TextType.ITALIC
            ),
            [TextNode("this is ", TextType.PLAIN), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.PLAIN)]
        )
    
    def test_code(self):
        old_nodes = [TextNode("this is `code`", TextType.PLAIN)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "`", 
                TextType.CODE
            ),
            [TextNode("this is ", TextType.PLAIN), TextNode("code", TextType.CODE)]
        )
    
    def test_raises_invalid_synthax(self):
        with self.assertRaises(Exception):
            old_nodes = [TextNode("this is invalid `code", TextType.PLAIN)]
            self.assertEqual(
                split_nodes_delimiter(
                    old_nodes, 
                    "`", 
                    TextType.CODE
                ),
                [TextNode("this is ", TextType.PLAIN), TextNode("code", TextType.CODE)]
            )
    
    def test_non_plain_node(self):
        old_nodes = [TextNode("this node is already bold", TextType.BOLD)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "**", 
                TextType.BOLD
            ),
            [TextNode("this node is already bold", TextType.BOLD)]
        )
    
    def test_multiple_delimiter_sets(self):
        old_nodes = [TextNode("that is **bold** but this is **bolder**", TextType.PLAIN)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "**", 
                TextType.BOLD
            ),
            [TextNode("that is ", TextType.PLAIN), TextNode("bold", TextType.BOLD), TextNode(" but this is ", TextType.PLAIN), TextNode("bolder", TextType.BOLD)]
        )
    
    def test_multiple_old_nodes(self):
        old_nodes = [TextNode("this is **bold**", TextType.PLAIN), TextNode("this is **bolder**", TextType.PLAIN)]
        self.assertEqual(
            split_nodes_delimiter(
                old_nodes, 
                "**", 
                TextType.BOLD
            ),
            [TextNode("this is ", TextType.PLAIN), TextNode("bold", TextType.BOLD), TextNode("this is ", TextType.PLAIN), TextNode("bolder", TextType.BOLD)]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
        [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

