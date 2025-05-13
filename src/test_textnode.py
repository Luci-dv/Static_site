import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_typenoteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_textnoteq(self):
        node = TextNode("This Is A Text Node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_urlnoteq(self):
        node = TextNode("This is a text node", TextType.LINK, "boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.wikipedia.org")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
    
    def test_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")
    
    def test_link(self):
        node = TextNode("This is a hyperlink", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a hyperlink")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "boot.dev")
    
    def test_image(self):
        node = TextNode("A cool turtle image", TextType.IMAGE, "www.wikipedia.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "www.wikipedia.org")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "A cool turtle image")
        self.assertEqual(html_node.value, "")
    
    def test_unsupported(self):
        node = TextNode("Bad link", "unsupported")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()