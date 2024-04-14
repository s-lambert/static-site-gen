import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_p(self):
    node = LeafNode("p", "This is a paragraph of text.")
    expected_html = "<p>This is a paragraph of text.</p>"
    self.assertEqual(node.to_html(), expected_html)
    
  def test_a(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    expected_html = "<a href=\"https://www.google.com\">Click me!</a>"
    self.assertEqual(node.to_html(), expected_html)

    
if __name__ == "__main__":
  unittest.main()