import unittest

from node.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a link node", TextType.LINK, None)
        node2 = TextNode("This is a link node", TextType.LINK)
        self.assertEqual(node.url, None)
        self.assertEqual(node2.url, None)

    def test_text_type(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        node2 = TextNode("This is a italic node", "italic")
        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a italic node", TextType.TEXT)
        node2 = TextNode("This is a bold node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a link node", TextType.LINK, "url/1")
        node2 = TextNode("This is a link node", TextType.LINK, "url/2")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
