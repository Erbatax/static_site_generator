import unittest

from html.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_empty_value_to_html(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_value_to_html(self):
        node = LeafNode(None, "This is a leaf node")
        self.assertEqual(node.to_html(), "This is a leaf node")

    def test_tag_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_props_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
