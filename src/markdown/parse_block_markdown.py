import enum
from functools import reduce
import re

from markdown.parse_inline_markdown import text_to_textnodes
from node.blocknode import BlockNode, BlockType
from node.textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    return list(
        filter(
            lambda block: block != "",
            map(lambda block: block.strip(), markdown.split("\n\n")),
        )
    )


def get_match_pattern(block_type):
    if block_type == BlockType.HEADING_1:
        return r"^#{1} (.*)"
    elif block_type == BlockType.HEADING_2:
        return r"^#{2} (.*)"
    elif block_type == BlockType.HEADING_3:
        return r"^#{3} (.*)"
    elif block_type == BlockType.HEADING_4:
        return r"^#{4} (.*)"
    elif block_type == BlockType.HEADING_5:
        return r"^#{5} (.*)"
    elif block_type == BlockType.HEADING_6:
        return r"^#{6} (.*)"
    elif block_type == BlockType.QUOTE:
        return r"^> ?(.*)"
    elif block_type == BlockType.UNORDERED_LIST:
        return r"^- ?(.*)"
    elif block_type == BlockType.ORDERED_LIST:
        return r"^(\d+)\. ?(.*)"
    else:
        return None


def match_markdown(block, block_type):
    if block_type == BlockType.CODE:
        lines = block.strip().split("\n")
        return (
            len(lines) > 1 and lines[0].strip() == "```" and lines[-1].strip() == "```"
        )
    return re.match(get_match_pattern(block_type), block)


def extract_markdown(block, block_type):
    if block_type in [BlockType.CODE]:
        lines = block.split("\n")
        return "\n".join(lines[1:-1])
    return re.findall(get_match_pattern(block_type), block)


def block_to_block_type(block):
    def true_for_all_line(test_function, block):
        return reduce(
            lambda acc, curr: acc and test_function(curr), block.split("\n"), True
        )

    if match_markdown(block, BlockType.HEADING_1):
        return BlockType.HEADING_1
    elif match_markdown(block, BlockType.HEADING_2):
        return BlockType.HEADING_2
    elif match_markdown(block, BlockType.HEADING_3):
        return BlockType.HEADING_3
    elif match_markdown(block, BlockType.HEADING_4):
        return BlockType.HEADING_4
    elif match_markdown(block, BlockType.HEADING_5):
        return BlockType.HEADING_5
    elif match_markdown(block, BlockType.HEADING_6):
        return BlockType.HEADING_6
    elif match_markdown(block, BlockType.CODE):
        return BlockType.CODE
    elif true_for_all_line(lambda line: match_markdown(line, BlockType.QUOTE), block):
        return BlockType.QUOTE
    elif true_for_all_line(
        lambda line: match_markdown(line, BlockType.UNORDERED_LIST), block
    ):
        return BlockType.UNORDERED_LIST
    elif true_for_all_line(
        lambda line: match_markdown(line, BlockType.ORDERED_LIST), block
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_block_node(block):
    block_type = block_to_block_type(block)

    if block_type in [
        BlockType.HEADING_1,
        BlockType.HEADING_2,
        BlockType.HEADING_3,
        BlockType.HEADING_4,
        BlockType.HEADING_5,
        BlockType.HEADING_6,
    ]:
        matches = extract_markdown(block, block_type)
        children = []
        for text in matches:
            children.extend(text_to_textnodes(text.strip()))
        return BlockNode(children, block_type)
    elif block_type == BlockType.CODE:
        text = extract_markdown(block, block_type)
        text = "\n".join([line.lstrip() for line in text.split("\n")])
        return BlockNode([TextNode(text, TextType.TEXT)], BlockType.CODE)
    elif block_type == BlockType.QUOTE:
        text_lines = []
        for line in block.split("\n"):
            matches = extract_markdown(line, BlockType.QUOTE)
            text_lines.extend(matches)
        block_text = "\n".join(text_lines)
        return BlockNode(
            text_to_textnodes(block_text),
            BlockType.QUOTE,
        )
    elif block_type == BlockType.UNORDERED_LIST:
        children = []
        for line in block.split("\n"):
            matches = extract_markdown(line, BlockType.UNORDERED_LIST)
            children.extend(
                [
                    BlockNode(
                        text_to_textnodes(text.strip()),
                        BlockType.UNORDERED_LIST_ITEM,
                    )
                    for text in matches
                ]
            )
        return BlockNode(
            children,
            BlockType.UNORDERED_LIST,
        )
    elif block_type == BlockType.ORDERED_LIST:
        children = []
        for line in block.split("\n"):
            matches = extract_markdown(line, BlockType.ORDERED_LIST)
            children.extend(
                [
                    BlockNode(
                        text_to_textnodes(text.strip()),
                        BlockType.ORDERED_LIST_ITEM,
                        {"number": int(number)},
                    )
                    for number, text in matches
                ]
            )
        return BlockNode(
            children,
            BlockType.ORDERED_LIST,
        )
    else:
        return BlockNode(text_to_textnodes(block.strip()), BlockType.PARAGRAPH)


def extract_title(markdown):
    block = markdown.split("\n\n")[0]
    if block_to_block_type(block) != BlockType.HEADING_1:
        raise Exception("First block is not a heading")
    return extract_markdown(block, BlockType.HEADING_1)[0]
