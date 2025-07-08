import unittest

from markdown.parse_block_markdown import (
    BlockType,
    block_to_block_node,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
)
from node.blocknode import BlockNode
from node.textnode import TextNode, TextType


class TestParseBlockMarkdown(unittest.TestCase):
    # region markdown_to_blocks
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

    def test_markdown_to_blocks_empty(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_line(self):
        markdown = "\n\n   Text surrounded by space   \n\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks, ["Text surrounded by space"])

    # endregion
    # region block_to_block_type
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING_1)

        block2 = "## This is a heading"
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING_2)

        block3 = "### This is a heading"
        self.assertEqual(block_to_block_type(block3), BlockType.HEADING_3)

        block4 = "#### This is a heading"
        self.assertEqual(block_to_block_type(block4), BlockType.HEADING_4)

        block5 = "##### This is a heading"
        self.assertEqual(block_to_block_type(block5), BlockType.HEADING_5)

        block6 = "###### This is a heading"
        self.assertEqual(block_to_block_type(block6), BlockType.HEADING_6)

    def test_block_to_block_type_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_multi_line(self):
        block = """
    ```
    This is text that _should_ remain
    the same even with inline stuff
    ```
    """
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_multi_line_quote(self):
        block = "> This is a quote\n> on multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_bad_multi_line_quote(self):
        block = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_multi_line_unordered_list(self):
        block = "- This is an unordered list\n- on multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_bad_multi_line_unordered_list(self):
        block = "- This is an unordered list\nThis is not an unordered list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_multi_line_ordered_list(self):
        block = "1. This is an ordered list\n2. on multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_bad_multi_line_ordered_list(self):
        block = "1. This is an ordered list\nThis is not an ordered list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # endregion
    # region block_to_block_node
    def test_block_to_block_node_empty(self):
        block = ""
        self.assertEqual(
            block_to_block_node(block),
            BlockNode([], BlockType.PARAGRAPH),
        )

    def test_block_to_block_node_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a paragraph", TextType.TEXT)], BlockType.PARAGRAPH
            ),
        )

    def test_block_to_block_node_heading(self):
        block = "# This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_1
            ),
        )

        block = "## This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_2
            ),
        )

        block = "### This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_3
            ),
        )

        block = "#### This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_4
            ),
        )

        block = "##### This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_5
            ),
        )

        block = "###### This is a heading"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a heading", TextType.TEXT)], BlockType.HEADING_6
            ),
        )

    def test_block_to_block_node_code(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a code block", TextType.TEXT)], BlockType.CODE
            ),
        )

        block = "```\nThis is a code block\non multiple lines\n```"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [TextNode("This is a code block\non multiple lines", TextType.TEXT)],
                BlockType.CODE,
            ),
        )

    #     block = """
    # ```
    # This is text that _should_ remain
    # the same even with inline stuff
    # ```
    # """
    #     self.assertEqual(
    #         block_to_block_node(block),
    #         BlockNode(
    #             [
    #                 TextNode(
    #                     "This is text that _should_ remain\nthe same even with inline stuff",
    #                     TextType.TEXT,
    #                 )
    #             ],
    #             BlockType.CODE,
    #         ),
    #     )

    def test_block_to_block_node_quote(self):
        block = "> This is a quote"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode([TextNode("This is a quote", TextType.TEXT)], BlockType.QUOTE),
        )

        block = "> This is a quote\n> on multiple lines"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [
                    TextNode("This is a quote", TextType.TEXT),
                    TextNode("\n", TextType.TEXT),
                    TextNode("on multiple lines", TextType.TEXT),
                ],
                BlockType.QUOTE,
            ),
        )

    def test_block_to_block_node_unordered_list(self):
        block = "- This is an unordered list"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [
                    BlockNode(
                        [TextNode("This is an unordered list", TextType.TEXT)],
                        BlockType.UNORDERED_LIST_ITEM,
                    )
                ],
                BlockType.UNORDERED_LIST,
            ),
        )

        block = "- This is an unordered list\n- on multiple lines"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [
                    BlockNode(
                        [TextNode("This is an unordered list", TextType.TEXT)],
                        BlockType.UNORDERED_LIST_ITEM,
                    ),
                    BlockNode(
                        [TextNode("on multiple lines", TextType.TEXT)],
                        BlockType.UNORDERED_LIST_ITEM,
                    ),
                ],
                BlockType.UNORDERED_LIST,
            ),
        )

    def test_block_to_block_node_ordered_list(self):
        block = "1. This is an ordered list"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [
                    BlockNode(
                        [TextNode("This is an ordered list", TextType.TEXT)],
                        BlockType.ORDERED_LIST_ITEM,
                        {"number": 1},
                    )
                ],
                BlockType.ORDERED_LIST,
            ),
        )

        block = "1. This is an ordered list\n2. on multiple lines"
        self.assertEqual(
            block_to_block_node(block),
            BlockNode(
                [
                    BlockNode(
                        [TextNode("This is an ordered list", TextType.TEXT)],
                        BlockType.ORDERED_LIST_ITEM,
                        {"number": 1},
                    ),
                    BlockNode(
                        [TextNode("on multiple lines", TextType.TEXT)],
                        BlockType.ORDERED_LIST_ITEM,
                        {"number": 2},
                    ),
                ],
                BlockType.ORDERED_LIST,
            ),
        )

    # endregion
    # region extract_title
    def test_extract_title(self):
        markdown = "# This is a title"
        self.assertEqual(extract_title(markdown), "This is a title")

        markdown = "# This is a title\n# on multiple lines"
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_extract_title_empty(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_no_title(self):
        markdown = "This is not a title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    # endregion


if __name__ == "__main__":
    unittest.main()
