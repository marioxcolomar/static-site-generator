import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"class": "bg-100", "disabled": "false"})
        self.assertEqual(' class="bg-100" disabled="false"', node.props_to_html())

    def test_to_html(self):
        try:
            node = HTMLNode(
                tag="a",
                value="me-anchor",
            )
            node.to_html()
        except Exception as e:
            print(f"Error in to_html: {e}")

    def test_values(self):
        value = "I wish I was a little bit taller"
        node = HTMLNode("div", value)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, value)

    def test_repr(self):
        node = HTMLNode("p", "I love Python!", props={"class": "bg-300"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, I love Python!, children: None, {'class': 'bg-300'})",
        )

    def test_leaf_to_html_p(self):
        leaf = LeafNode("p", "Hello, World!")
        self.assertEqual(leaf.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_a(self):
        leaf = LeafNode("a", "Hello, World!", {"href": "https://hello.world"})
        self.assertEqual(
            leaf.to_html(), '<a href="https://hello.world">Hello, World!</a>'
        )

    def test_to_html_children(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        print(f"this is parent: {parent.to_html()}")


if __name__ == "__main___":
    unittest.main()
