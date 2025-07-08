from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING_1 = "heading1"
    HEADING_2 = "heading2"
    HEADING_3 = "heading3"
    HEADING_4 = "heading4"
    HEADING_5 = "heading5"
    HEADING_6 = "heading6"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    UNORDERED_LIST_ITEM = "unordered_list_item"
    ORDERED_LIST = "ordered_list"
    ORDERED_LIST_ITEM = "ordered_list_item"


class BlockNode:
    def __init__(self, children, block_type, props=None):
        self.children = children
        self.block_type = BlockType(block_type)
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, BlockNode):
            return False
        return (
            self.children == other.children
            and self.block_type == other.block_type
            and self.props == other.props
        )

    def __repr__(self):
        return f"BlockNode({self.children}, {self.block_type.value}, {self.props})"
