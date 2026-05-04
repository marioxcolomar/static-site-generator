import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = "# Heading"
        heading = block_to_block_type(md)
        self.assertEqual(heading, BlockType.HEADING)

        code_md = "```\nme code very nice\n```"
        code = block_to_block_type(code_md)
        self.assertEqual(code, BlockType.CODE)

        quote_md = "> Best quote.\n> By somebody"
        quote = block_to_block_type(quote_md)
        self.assertEqual(quote, BlockType.QUOTE)

        unordered_list_md = "- Bananas\n- Rice"
        unordered_list = block_to_block_type(unordered_list_md)
        self.assertEqual(unordered_list, BlockType.U_LIST)

        ordered_list_md = "1. Breakfast\n2. Lunch\n3. Dinner"
        order_list = block_to_block_type(ordered_list_md)
        self.assertEqual(order_list, BlockType.O_LIST)

        text = "a paragraph"
        text_type = block_to_block_type(text)
        self.assertEqual(text_type, BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p tag

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extrat_title(self):
        md = "# Hello "
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_extract_title_multiple_lines(self):
        md = "# Me title\nWith more lines\nTesting testing"
        title = extract_title(md)
        self.assertEqual(title, "Me title")


if __name__ == "__main__":
    unittest.main()
