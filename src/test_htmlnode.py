import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test1(self):
        Child1 = HTMLNode("this is a child tag", "this is a child value")
        Child2 = HTMLNode("this is a child tag", "this is a child value")
        children = [Child1, Child2]
        props = {"key1": "value1", "key2": "value2"}
        Node = HTMLNode("this is a tag", "this is a value", children, props)
        print(Node.props_to_html())

    def test2(self):
        Child1 = HTMLNode("this is a child tag", "this is a child value")
        Child2 = HTMLNode("this is a child tag", "this is a child value")
        children = [Child1, Child2]
        props = {"key1": "value1", "key2": "value2"}
        Node = HTMLNode("this is a tag", "this is a value", children, props)
        print(Node)
    
    def test3(self):
        Node = HTMLNode()
        print(Node)
    
    def test4(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test5(self):
        node = LeafNode("a", "Welcome to Boot.dev!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Welcome to Boot.dev!</a>')
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_2_children(self):
        child_node1 = LeafNode("b", "child1")
        child_node2 = LeafNode("i", "child2")
        parent_node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>child1</b><i>child2</i></p>",
        )

    def test_to_html_tag_raises_value_error(self):
        with self.assertRaises(ValueError):    
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            html_string = parent_node.to_html()

    def test_to_html_children_raises_value_error1(self):
        with self.assertRaises(ValueError):    
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("p", None)
            html_string = parent_node.to_html()

    def test_to_html_children_raises_value_error2(self):
        with self.assertRaises(ValueError):    
            child_node = LeafNode("span", "child")
            parent_node = ParentNode("p", [])
            html_string = parent_node.to_html()

    def test_to_html_with_props(self):     
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"key1": "value1"})
        self.assertEqual(parent_node.to_html(), '<div key1="value1"><span>child</span></div>')