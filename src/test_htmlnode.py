import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
  def test_anchor_eq(self):
    node = HtmlNode("a", None, None, { "href": "https://example.com", "target": "__blank" })
    node2 = HtmlNode("a", None, None, { "href": "https://example.com", "target": "__blank" })
    self.assertEqual(node, node2)
  
  def test_with_children(self):
    node = HtmlNode(
      "div", 
      None, 
      [HtmlNode("a", None, None, { "href": "https://example.com", "target": "__blank" })], 
      None)
    html = node.to_html()
    self.assertIn("div", html)
    self.assertIn("<a", html)
  
  def test_with_text(self):
    node = HtmlNode(
      "span",
      "Hello World!",
      None,
      { "class": "font-normal" }
    )
    html = node.to_html()
    self.assertIn("span", html)
    self.assertIn("class=\"font-normal\"", html)
    self.assertIn("Hello World!", html)

if __name__ == "__main__":
  unittest.main()