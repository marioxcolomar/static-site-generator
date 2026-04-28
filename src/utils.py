import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        positions = node.text.split(delimiter)
        if len(positions) % 2 == 0:
            raise Exception(
                "Error: invalid Markdown syntax, formatted section did not close."
            )

        for i in range(len(positions)):
            if positions[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(positions[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(positions[i], text_type))

        new_nodes.extend(split_nodes)

        return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links
