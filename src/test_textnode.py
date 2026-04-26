import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_wrong_type(self):
        try:
            node = TextNode("Wrong type", "wrong")
            print(node)
        except Exception as e:
            print(f"Error in type: {e}")

    def test_not_eq(self):
        node = TextNode("This is a unique text", TextType.BOLD)
        node2 = TextNode("This is also a unique text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
