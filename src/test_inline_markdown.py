import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delim_italic_and_code(self):
        node = TextNode("This is _italic_ with `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ],
        )

    def test_markdown_images_extract(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png). This is a bad format ![picture](not-a-link)",
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("picture", "not-a-link")],
            matches,
        )

    def test_markdown_links_extract(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.link.com). More link would be [great](https://great.com)"
        )
        self.assertListEqual(
            [("link", "https://www.link.com"), ("great", "https://great.com")], matches
        )

    def test_split_image(self):
        node = TextNode(
            "This text has an ![image](https://i.imgur.com/zjj123.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjj123.png"),
            ],
            new_nodes,
        )

    def test_split_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjj123.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjj123.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This text has an ![image](https://i.imgur.com/zjj123.png) and another ![picture](https://my-picture.com/123.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text has an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjj123.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("picture", TextType.IMAGE, "https://my-picture.com/123.png"),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode("Some text with a [link](https://me-link.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Some text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://me-link.com"),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode("[link](https://me-link.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://me-link.com")], new_nodes
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "Some text with a [link](https://me-link.com) and another [super link](https://super-link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Some text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://me-link.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("super link", TextType.LINK, "https://super-link.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
