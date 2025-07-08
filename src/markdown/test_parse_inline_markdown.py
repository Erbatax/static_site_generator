import unittest

from markdown.parse_inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from node.textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    # region split_node
    def test_split_node_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_node_with_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_split_node_with_italics(self):
        node = TextNode(
            "This is text with a _italics phrase_ in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italics phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.TEXT),
            ],
        )

    def test_split_node_with_italic_bold(self):
        node = TextNode("This is an _italic and **bold** word_.", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter([node], "_", TextType.ITALIC), "**", TextType.BOLD
        )
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode(
                    "italic and **bold** word",
                    TextType.ITALIC,
                ),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_node_unbalanced(self):
        node = TextNode(
            "This is text with a **bolded phrase* in the middle", TextType.TEXT
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_node_balanced(self):
        node_bold = TextNode(
            "**This is text within a complete bolded phrase**", TextType.TEXT
        )
        node_bold_at_start = TextNode(
            "**This is bolded text** within a phrase", TextType.TEXT
        )
        node_bold_at_end = TextNode(
            "This is text with a **bolded phrase**", TextType.TEXT
        )

        self.assertEqual(
            split_nodes_delimiter([node_bold], "**", TextType.BOLD),
            [
                TextNode("This is text within a complete bolded phrase", TextType.BOLD),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter([node_bold_at_start], "**", TextType.BOLD),
            [
                TextNode("This is bolded text", TextType.BOLD),
                TextNode(" within a phrase", TextType.TEXT),
            ],
        )
        self.assertEqual(
            split_nodes_delimiter([node_bold_at_end], "**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
            ],
        )

    # endregion
    # region extract_markdown_images and extract_markdown_links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_images_and_links(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches
        )
        self.assertListEqual([("link", "https://www.google.com")], link_matches)

    # endregion
    # region split_images
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_only_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    # endregion
    # region split_links
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_with_only_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                    TextType.TEXT,
                ),
            ],
            new_nodes,
        )

    # endregion
    # region text_to_textnodes
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, nodes)

    def test_text_to_textnodes_with_only_raw_text(self):
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        expected_nodes = [
            TextNode(text, TextType.TEXT),
        ]

        nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, nodes)

    def test_text_to_textnodes_with_empty_text(self):
        text = ""
        expected_nodes = []

        nodes = text_to_textnodes(text)
        self.assertListEqual(expected_nodes, nodes)

    # endregion
