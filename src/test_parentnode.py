import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
  def test_with_children(self):
    node = ParentNode(
      "p",
      [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
      ],
    )
    expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    self.assertEqual(node.to_html(), expected_html)
    
  def test_nested_children(self):
    node = ParentNode(
      "div",
      [
        ParentNode(
          "p",
          [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
          ],
        ),
      ]
    )
    expected_html = "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
    self.assertEqual(node.to_html(), expected_html)