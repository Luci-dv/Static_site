from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type, all_delimiters=None):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        pieces = old_node.text.split(delimiter)
        if len(pieces) == 1:
            result.append(old_node)
            continue

        if len(pieces) % 2 == 0:
            raise ValueError(f"No closing delimiter found for {delimiter}")

        for i in range(len(pieces)):
            if i == 0:
                if pieces[i]:
                    result.append(TextNode(pieces[i], TextType.TEXT))
            elif i % 2 == 1:
                delimited_content = pieces[i]

                if all_delimiters and len(all_delimiters) > 0:
                    inner_node = TextNode(delimited_content, TextType.TEXT)
                    next_delimiter, next_type = all_delimiters[0]
                    remaining_delimiters = all_delimiters[1:]
                    processed_nodes = split_nodes_delimiter([inner_node], next_delimiter, next_type, remaining_delimiters)

                    for node in processed_nodes:
                        if node.text_type == TextType.TEXT:
                            result.append(TextNode(node.text, text_type))
                        else:
                            result.append(node)
                    
                else:
                    result.append(TextNode(delimited_content, text_type))
            else:
                if pieces[i]:
                    result.append(TextNode(pieces[i], TextType.TEXT))