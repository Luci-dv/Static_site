from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    after_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            text = node.text
            start_index = text.find(delimiter)
            if start_index == -1:
                result.append(node)
                continue
            end_index = text.find(delimiter, start_index+len(delimiter))
            if end_index == -1:
                raise ValueError(f"No closing delimiter found for {delimiter}")
            
            before_text = text[:start_index]
            delimited_text = text[start_index + len(delimiter):end_index]
            after_text = text[end_index + len(delimiter):]

            if before_text:
                result.append(TextNode(before_text, TextType.TEXT))
            result.append(TextNode(delimited_text, text_type))
            after_nodes = split_nodes_delimiter([TextNode(after_text, TextType.TEXT)], delimiter, text_type)
            result.extend(after_nodes)
        else:
            result.append(node)
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)
        if extracted:
            alt_text, url = extracted[0]
            delimiter = f"![{alt_text}]({url})"
            parts = node.text.split(delimiter, 1)

            if parts[0]:
                text = TextNode(parts[0], TextType.TEXT)
                result.append(text)
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            if parts[1]:
                remaining_nodes = split_nodes_image([TextNode(parts[1], TextType.TEXT)])
                result.extend(remaining_nodes)
        else:
            result.append(node)
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        extracted = extract_markdown_links(node.text)
        if extracted:
            text, link = extracted[0]
            delimiter = f"[{text}]({link})"
            parts = node.text.split(delimiter, 1)

            if parts[0]:
                before_text = TextNode(parts[0], TextType.TEXT)
                result.append(before_text)
            result.append(TextNode(text, TextType.LINK, link))
            if parts[1]:
                remaining_nodes = split_nodes_link([TextNode(parts[1], TextType.TEXT)])
                result.extend(remaining_nodes)
        else:
            result.append(node)
    return result