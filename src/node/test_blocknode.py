import unittest

from node.blocknode import BlockNode, BlockType


class TestBlockNode(unittest.TestCase):
    def test_eq(self):
        node = BlockNode("This is a block node", BlockType.PARAGRAPH)
        node2 = BlockNode("This is a block node", BlockType.PARAGRAPH)
        self.assertEqual(node, node2)

    def test_different_block(self):
        node = BlockNode("This is a header node", BlockType.PARAGRAPH)
        node2 = BlockNode("This is a code node", BlockType.PARAGRAPH)
        self.assertNotEqual(node, node2)

    def test_different_block_type(self):
        node = BlockNode("This is a block node", BlockType.HEADING_1)
        node2 = BlockNode("This is a block node", BlockType.CODE)
        self.assertNotEqual(node, node2)

    def test_different_props(self):
        node = BlockNode(
            "This is a block node", BlockType.ORDERED_LIST_ITEM, {"number": "1"}
        )
        node2 = BlockNode(
            "This is a block node", BlockType.ORDERED_LIST_ITEM, {"number": "2"}
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
