import unittest
from text_parser import text_to_textnodes, markdown_to_blocks, extract_title
from textnode import TextNode, TextType

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_bold_text(self):
        text = "This is text with **bold** formatting"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is text with ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " formatting")
    
    def test_multiple_formats(self):
        text = "This is text with _italic_ and **bold** formatting, and a `code block`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[3].text, "bold")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
    
    def test_link_and_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)![Rick Astley](https://i.imgur.com/rickroll)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[2].text_type, TextType.IMAGE)
    
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
    
    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_excessive_newline(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
    
    def test_markdown_to_blocks_different_markdown_types(self):
        md = "# Heading\n\n```\ncode block\n```\n\n- List item 1\n- List item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "```\ncode block\n```", "- List item 1\n- List item 2"])
    
    def test_extract_title(self):
        md = "# Heading\n\n```\ncode block\n```\n\n- List item 1\n- List item 2"
        title = extract_title(md)
        self.assertEqual(title, "Heading")
    
    def test_extract_notitle(self):
        md = "### Heading\n\n```\ncode block\n```\n\n- List item 1\n- List item 2"
        with self.assertRaises(Exception):
            extract_title(md)
