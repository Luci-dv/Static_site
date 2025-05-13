import unittest
from block_to_html import markdown_to_html_node

class TestBlockNodesToHTML(unittest.TestCase):
    
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
    
    def test_mixed_with_heading(self):
        md = """
        ## This is the heading at H2

        This paragraph should work, including the _italics_

        ```
        This code block should also pass
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is the heading at H2</h2><p>This paragraph should work, including the <i>italics</i></p><pre><code>This code block should also pass\n</code></pre></div>"
        )
    
    def test_quotes_and_lists(self):
        md = """
        # This is the heading

        >Famous Quote
        >Sun Tzu

        - Might need to fix things later
        - Hopefully this works

        1. Final List
        2. C'mon pass this **please**
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is the heading</h1><blockquote>Famous Quote Sun Tzu</blockquote><ul><li>Might need to fix things later</li><li>Hopefully this works</li></ul><ol><li>Final List</li><li>C'mon pass this <b>please</b></li></ol></div>"
        )