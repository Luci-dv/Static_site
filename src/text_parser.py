from textnode import TextNode, TextType
from nodefunctions import *

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    document = markdown.strip()
    blocks = document.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        lines = block.split("\n")
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block = "\n".join(cleaned_lines)
        if cleaned_block != "":
            cleaned_blocks.append(cleaned_block)
    return cleaned_blocks

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            tag, text = line.split(" ", 1)
            cleaned_title = text.strip()
            return cleaned_title
    raise Exception("No title found")

