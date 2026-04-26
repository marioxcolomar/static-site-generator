from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        match = self.text_type == other.text_type
        if match:
            return True
        return False

    def text_node_to_html_node(self, text_node):
        match TextType(text_node):
            case TextType.TEXT:
                return LeafNode(None, text_node.text)

            case TextType.BOLD:
                return LeafNode("b", text_node.text)

            case TextType.ITALIC:
                return LeafNode("i", text_node.text)

            case TextType.CODE:
                return LeafNode("code", text_node.text)

            case TextType.LINK:
                return LeafNode("a", text_node.text)

            case _:
                raise Exception(f"Error: text node unknown {text_node}")

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
