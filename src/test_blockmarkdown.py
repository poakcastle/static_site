import unittest
from blockmarkdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_excess_newlines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type_paragraph(self):
        md = "this is a paragraph\nwith multiple lines"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        md = "#### heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        md = ">I am become death, the destroyer of world\n> I don't like sand. It's coarse and irritating and it gets everywhere."
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_block_to_block_type_unordered(self):
        md = "- object\n- next object\n- other object"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED)
    
    def test_block_to_block_type_ordered(self):
        md = "1. object\n2. next object\n3. other object"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED)
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
