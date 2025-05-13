from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def block_to_block_type(block):
    if not block:
        raise Exception("Empty block - input not accepted")
    lines = block.split("\n")
    if len(lines) == 1:
        heading_text = lines[0].split(" ", 1)
        if 1 <= len(heading_text[0]) <= 6 and set(heading_text[0]) == {"#"} and heading_text[1] and not heading_text[1].startswith(" "):
            return BlockType.HEADING
    if lines[0] == "```" and lines[-1] == "```" and any(line.strip() for line in lines[1:-1]):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED
    if all(line.startswith(f"{idx}. ") for idx, line in enumerate(lines, start=1)):
        return BlockType.ORDERED
    return BlockType.PARAGRAPH
