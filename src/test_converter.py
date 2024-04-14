import unittest

from textnode import TextNode
from converter import split_nodes_delimiter


class TestConverter(unittest.TestCase):
  def test_node_splitter(self):
    node = TextNode("This is text with a `code block` word", "text")
    new_nodes = split_nodes_delimiter([node], "`", "code")
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", "text"),
        TextNode("code block", "code"),
        TextNode(" word", "text"),
      ]
    )
  
  def test_multiple_bold(self):
    node = TextNode("This is text with a **bold** word and **more bold** words", "text")
    new_nodes = split_nodes_delimiter([node], "**", "bold")
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", "text"),
        TextNode("bold", "bold"),
        TextNode(" word and ", "text"),
        TextNode("more bold", "bold"),
        TextNode(" words", "text"),
      ]
    )
    

if __name__ == "__main__":
    unittest.main()