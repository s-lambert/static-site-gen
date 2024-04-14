import unittest

from textnode import TextNode
from converter import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestConverter(unittest.TestCase):
  def test_text_to_nodes(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    text_nodes = text_to_textnodes(text)
    self.assertEqual(
      text_nodes,
      [
        TextNode("This is ", "text"),
        TextNode("text", "bold"),
        TextNode(" with an ", "text"),
        TextNode("italic", "italic"),
        TextNode(" word and a ", "text"),
        TextNode("code block", "code"),
        TextNode(" and an ", "text"),
        TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and a ", "text"),
        TextNode("link", "link", "https://boot.dev"),
      ]
    )
  
  def test_delimiter_splitter(self):
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
    
  def test_image_splitter(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      "text",
    )
    new_nodes = split_nodes_image([node])
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with an ", "text"),
        TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and another ", "text"),
        TextNode(
          "second image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        ),
      ]
    )
  
  def test_no_images(self):
    node = TextNode(
      "This is text",
      "text",
    )
    new_nodes = split_nodes_image([node])
    self.assertEqual(
      new_nodes,
      [TextNode("This is text", "text")]
    )
  
  def test_link_splitter(self):
    node = TextNode(
      "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      "text",
    )
    new_nodes = split_nodes_link([node])
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", "text"),
        TextNode("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
        TextNode(" and another ", "text"),
        TextNode(
          "second link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
        ),
      ]
    )
  
    
  def test_image_extraction(self):
    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    extracted_images = extract_markdown_images(text)
    expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
    self.assertEqual(extracted_images, expected)

  def test_link_extraction(self):
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    extracted_links = extract_markdown_links(text)
    expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
    self.assertEqual(extracted_links, expected)
    
  def test_no_links(self):
    self.assertEqual(extract_markdown_links("foo bar baz"), [])
    self.assertEqual(extract_markdown_images("foo bar baz"), [])
    

if __name__ == "__main__":
    unittest.main()