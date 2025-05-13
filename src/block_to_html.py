from text_parser import *
from blocktype import *
from textnode import *
from htmlnode import *

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.CODE:
            text = "\n".join(block.split("\n")[1:-1])
            if not text.endswith("\n"):
                text = text + "\n"
            node = TextNode(text, TextType.CODE)
            html = text_node_to_html_node(node)
            codenode = ParentNode("pre", [html])
            children.append(codenode)
        if blocktype == BlockType.HEADING:
            prefix, text = block.split(" ", 1)
            count = len(prefix)
            nodes = text_to_textnodes(text)
            htmlnodes = inline_transform(nodes)
            headingnode = ParentNode(f"h{count}", htmlnodes)
            children.append(headingnode)
        if blocktype == BlockType.UNORDERED:
            lines = block.split("\n")
            htmlitems = []
            for line in lines:
                prefix, text = line.split(" ", 1)
                nodes = text_to_textnodes(text)
                htmlnodes = inline_transform(nodes)
                listitems = ParentNode("li", htmlnodes)
                htmlitems.append(listitems)
            unorderednode = ParentNode("ul", htmlitems)
            children.append(unorderednode)
        if blocktype == BlockType.ORDERED:
            lines = block.split("\n")
            htmlitems = []
            for line in lines:
                prefix, text = line.split(" ", 1)
                nodes = text_to_textnodes(text)
                htmlnodes = inline_transform(nodes)
                listitems = ParentNode("li", htmlnodes)
                htmlitems.append(listitems)
            orderednode = ParentNode("ol", htmlitems)
            children.append(orderednode)
        if blocktype == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned = []
            for line in lines:
                text = line.lstrip("> ")
                cleaned.append(text)
            textblock = " ".join(cleaned)
            nodes = text_to_textnodes(textblock)
            htmlnodes = inline_transform(nodes)
            quoteitems = ParentNode("blockquote", htmlnodes)
            children.append(quoteitems)
        if blocktype == BlockType.PARAGRAPH:
            text = block.replace("\n", " ")
            nodes = text_to_textnodes(text)
            htmlnodes = inline_transform(nodes)
            paragraphnode = ParentNode("p", htmlnodes)
            children.append(paragraphnode)
    finalnode = ParentNode("div", children)
    return finalnode
        



def inline_transform(nodes):
    htmlnodes = []
    for node in nodes:
        html = text_node_to_html_node(node)
        htmlnodes.append(html)
    return htmlnodes
