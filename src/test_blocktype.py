import unittest

from blocktype import block_to_block_type, BlockType

class TestBLOCKTYPE(unittest.TestCase):
    def test_null(self):
        block = ""
        with self.assertRaises(Exception):
            block_to_block_type(block)
    
    def test_heading(self):
        block = "## This is a heading"
        blockformat = block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.HEADING)
    
    def test_heading_overassigned(self):
        block = "######## This is a paragraph"
        blockformat = block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.PARAGRAPH)
    
    def test_codeblock(self):
        block = "```\nCODE GOES HERE\n```"
        blockformat = block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.CODE)
        block2 = "```\n```"
        block2format = block_to_block_type(block2)
        self.assertEqual(block2format, BlockType.PARAGRAPH)
        block3 = "```\n   \n```"
        block3format = block_to_block_type(block3)
        self.assertEqual(block3format, BlockType.PARAGRAPH)
    
    def test_quotes(self):
        block = ">Quote Block\n>mfw it works\n>i.imgur.com/yahoo.png"
        blockformat = block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.QUOTE)
        block2 = ">Quote Block\n Whoops missed the marker\n>Nah it'll work right???"
        block2format = block_to_block_type(block2)
        self.assertEqual(block2format, BlockType.PARAGRAPH)
    
    def test_list_unordered(self):
        block = "- List of tests\n- Don't forget list blocks\n- Make it more ordered"
        blockformat =block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.UNORDERED)
        block2 = "-List 2\n2. Hmmm...\n- This is a mess!"
        block2format = block_to_block_type(block2)
        self.assertEqual(block2format, BlockType.PARAGRAPH)
    
    def test_list_ordered(self):
        block = "1. Ordered list\n2. All elements in correct order\n3. This should pass"
        blockformat = block_to_block_type(block)
        self.assertEqual(blockformat, BlockType.ORDERED)
        block2 = "2. Ordered list\n1. Wait I forgot 1\n3. This won't work?"
        block2format = block_to_block_type(block2)
        self.assertEqual(block2format, BlockType.PARAGRAPH)