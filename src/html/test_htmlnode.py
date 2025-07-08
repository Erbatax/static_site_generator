import unittest

from html.htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_empty_props_to_html(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_to_html(self):
        node = HTMLNode(
            tag="a",
            value="This is a link",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">This is a link</a>',
        )

    def test_to_html_without_props(self):
        node = HTMLNode(tag="a", value="This is a link")
        self.assertEqual(node.to_html(), "<a>This is a link</a>")


if __name__ == "__main__":
    unittest.main()
