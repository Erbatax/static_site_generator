import unittest

from html.htmlnode import HTMLNode
from html.leafnode import LeafNode
from html.parentnode import ParentNode
from html.textNodeToHtmlNode import block_node_to_html_node, text_node_to_html_node
from node.blocknode import BlockNode, BlockType
from node.textnode import TextNode, TextType


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        self.assertEqual(html_node.to_html(), "<i>This is a italic node</i>")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.google.com">This is a link node</a>',
        )

    def test_image(self):
        node = TextNode(
            "This is a image node", TextType.IMAGE, "https://www.google.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.google.com")
        self.assertEqual(html_node.props["alt"], "This is a image node")
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://www.google.com" alt="This is a image node" />',
        )


class TestBlockNodeToHtmlNode(unittest.TestCase):
    def test_empty(self):
        node = BlockNode([], BlockType.PARAGRAPH)
        html_node = block_node_to_html_node(node)
        self.assertEqual(html_node, ParentNode("p", []))

    def test_paragraph(self):
        node = BlockNode(
            [TextNode("This is a paragraph", TextType.TEXT)], BlockType.PARAGRAPH
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("p", [LeafNode(None, "This is a paragraph")])
        )
        self.assertEqual(html_node.to_html(), "<p>This is a paragraph</p>")

    def test_heading_1(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_1
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h1", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h1>This is a heading</h1>")

    def test_heading_2(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_2
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h2", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h2>This is a heading</h2>")

    def test_heading_3(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_3
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h3", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h3>This is a heading</h3>")

    def test_heading_4(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_4
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h4", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h4>This is a heading</h4>")

    def test_heading_5(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_5
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h5", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h5>This is a heading</h5>")

    def test_heading_6(self):
        node = BlockNode(
            [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_6
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node, ParentNode("h6", [LeafNode(None, "This is a heading")])
        )
        self.assertEqual(html_node.to_html(), "<h6>This is a heading</h6>")

    def test_blockquote(self):
        node = BlockNode(
            [TextNode("This is a blockquote", TextType.TEXT)], BlockType.QUOTE
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode("blockquote", [LeafNode(None, "This is a blockquote")]),
        )
        self.assertEqual(
            html_node.to_html(), "<blockquote>This is a blockquote</blockquote>"
        )

    def test_unordered_list_item(self):
        node = BlockNode(
            [TextNode("This is a unordered list item", TextType.TEXT)],
            BlockType.UNORDERED_LIST_ITEM,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode("li", [LeafNode(None, "This is a unordered list item")]),
        )
        self.assertEqual(html_node.to_html(), "<li>This is a unordered list item</li>")

    def test_unordered_list(self):
        node = BlockNode(
            [
                BlockNode(
                    [TextNode("This is a unordered list", TextType.TEXT)],
                    BlockType.UNORDERED_LIST_ITEM,
                )
            ],
            BlockType.UNORDERED_LIST,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode(
                "ul", [ParentNode("li", [LeafNode(None, "This is a unordered list")])]
            ),
        )
        self.assertEqual(
            html_node.to_html(), "<ul><li>This is a unordered list</li></ul>"
        )

    def test_unordered_list_multiple_items(self):
        node = BlockNode(
            [
                BlockNode(
                    [TextNode("This is a unordered list", TextType.TEXT)],
                    BlockType.UNORDERED_LIST_ITEM,
                ),
                BlockNode(
                    [TextNode("with multiple items", TextType.TEXT)],
                    BlockType.UNORDERED_LIST_ITEM,
                ),
            ],
            BlockType.UNORDERED_LIST,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "This is a unordered list")]),
                    ParentNode("li", [LeafNode(None, "with multiple items")]),
                ],
            ),
        )
        self.assertEqual(
            html_node.to_html(),
            "<ul><li>This is a unordered list</li><li>with multiple items</li></ul>",
        )

    def test_ordered_list_item(self):
        node = BlockNode(
            [
                BlockNode(
                    [TextNode("This is a ordered list item", TextType.TEXT)],
                    BlockType.ORDERED_LIST_ITEM,
                )
            ],
            BlockType.ORDERED_LIST,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode(
                "ol",
                [ParentNode("li", [LeafNode(None, "This is a ordered list item")])],
            ),
        )
        self.assertEqual(
            html_node.to_html(),
            "<ol><li>This is a ordered list item</li></ol>",
        )

    def test_ordered_list(self):
        node = BlockNode(
            [
                BlockNode(
                    [TextNode("This is a ordered list", TextType.TEXT)],
                    BlockType.ORDERED_LIST_ITEM,
                )
            ],
            BlockType.ORDERED_LIST,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode(
                "ol", [ParentNode("li", [LeafNode(None, "This is a ordered list")])]
            ),
        )
        self.assertEqual(
            html_node.to_html(), "<ol><li>This is a ordered list</li></ol>"
        )

    def test_order_list_multiple_items(self):
        node = BlockNode(
            [
                BlockNode(
                    [TextNode("This is a ordered list", TextType.TEXT)],
                    BlockType.ORDERED_LIST_ITEM,
                ),
                BlockNode(
                    [TextNode("with multiple items", TextType.TEXT)],
                    BlockType.ORDERED_LIST_ITEM,
                ),
            ],
            BlockType.ORDERED_LIST,
        )

        html_node = block_node_to_html_node(node)
        self.assertEqual(
            html_node,
            ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, "This is a ordered list")]),
                    ParentNode("li", [LeafNode(None, "with multiple items")]),
                ],
            ),
        )
        self.assertEqual(
            html_node.to_html(),
            "<ol><li>This is a ordered list</li><li>with multiple items</li></ol>",
        )
