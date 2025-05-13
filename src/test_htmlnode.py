import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)
    
    def test_tagnoteq(self):
        node = HTMLNode("h1")
        node2 = HTMLNode("p")
        self.assertNotEqual(node, node2)
    
    def test_valuenoteq(self):
        node = HTMLNode("h1", "text")
        node2 = HTMLNode("h1", "Lorem Ipsum")
        self.assertNotEqual(node, node2)
    
    def test_childrennoteq(self):
        node = HTMLNode("h1", "Lorem Ipsum")
        node2 = HTMLNode("h1", "Lorem Ipsum", [node])
        node3 = HTMLNode("h1", "Lorem Ipsum", [node, node2])
        self.assertNotEqual(node2, node3)

    def test_propsnoteq(self):
        node = HTMLNode(None, None, None, {})
        node2 = HTMLNode(None, None, None, {"href": "https://boot.dev"})
        self.assertNotEqual(node, node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_leaf_node_no_value(self):
        # This should raise a ValueError
        with self.assertRaises(ValueError):
            LeafNode("p", None)
        
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
    
    def test_to_html_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("h1", "child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><h1>child</h1></div>"
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("h1", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )