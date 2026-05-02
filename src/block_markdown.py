from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list"
    O_LIST = "ORDERED_LIST"


def markdown_to_blocks(markdown):
    res = []
    sections = markdown.split("\n\n")
    for section in sections:
        if section == "":
            continue
        res.append(section.strip("\n"))
    return res


def block_to_block_type(markdown):
    lines = markdown.split("\n")
    # all heading types
    if markdown.startswith(("# ", "## ", "### ", "#### ", "#####", "######")):
        return BlockType.HEADING
    # code block at the start and end
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    # quote all lines start the same
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # unordered list
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.U_LIST
    # ordered list
    if markdown.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.O_LIST
    # none of the above means normal paragraph
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    type = block_to_block_type(block)
    if type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if type == BlockType.HEADING:
        return heading_to_html_node(block)
    if type == BlockType.CODE:
        return code_to_html_node(block)
    if type == BlockType.O_LIST:
        return o_list_to_html_node(block)
    if type == BlockType.U_LIST:
        return u_list_to_html_node(block)
    if type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError(f"block type not recognized: {type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def o_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = items.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def u_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
