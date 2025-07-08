from html.leafnode import LeafNode
from html.parentnode import ParentNode
from markdown.parse_block_markdown import (
    BlockType,
    block_to_block_type,
    extract_markdown,
)
from node.textnode import TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text,
                },
            )


def block_node_to_html_node(block_node):
    if block_node.block_type == BlockType.HEADING_1:
        return ParentNode(
            f"h1", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.HEADING_2:
        return ParentNode(
            f"h2", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.HEADING_3:
        return ParentNode(
            f"h3", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.HEADING_4:
        return ParentNode(
            f"h4", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.HEADING_5:
        return ParentNode(
            f"h5", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.HEADING_6:
        return ParentNode(
            f"h6", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.CODE:
        return ParentNode(
            "pre",
            ParentNode("code", LeafNode(None, block_node.children[0].text + "\n")),
        )
    elif block_node.block_type == BlockType.QUOTE:
        return ParentNode(
            "blockquote",
            [text_node_to_html_node(child) for child in block_node.children],
        )
    elif block_node.block_type == BlockType.UNORDERED_LIST:
        return ParentNode(
            "ul",
            [block_node_to_html_node(child) for child in block_node.children],
        )
    elif block_node.block_type == BlockType.UNORDERED_LIST_ITEM:
        return ParentNode(
            "li", [text_node_to_html_node(child) for child in block_node.children]
        )
    elif block_node.block_type == BlockType.ORDERED_LIST:
        return ParentNode(
            "ol",
            [block_node_to_html_node(child) for child in block_node.children],
        )
    elif block_node.block_type == BlockType.ORDERED_LIST_ITEM:
        return ParentNode(
            "li", [text_node_to_html_node(child) for child in block_node.children]
        )
    else:
        return ParentNode(
            "p", [text_node_to_html_node(child) for child in block_node.children]
        )
