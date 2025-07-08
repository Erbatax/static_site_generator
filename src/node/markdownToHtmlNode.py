from html.parentnode import ParentNode
from html.textNodeToHtmlNode import block_node_to_html_node
from markdown.parse_block_markdown import (
    block_to_block_node,
    markdown_to_blocks,
)
from markdown.parse_inline_markdown import text_to_textnodes


def text_to_children(text):
    text_to_textnodes(text)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    blockNodes = [block_to_block_node(block) for block in blocks]
    htmlNodes = [block_node_to_html_node(blockNode) for blockNode in blockNodes]

    return ParentNode("div", children=htmlNodes)
