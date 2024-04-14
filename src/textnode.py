from leafnode import LeafNode


class TextNode:
  def __init__(self, text, text_type, url=None):
    self.__text = text
    self.__text_type = text_type
    self.__url = url
    
  def to_html_node(self):
    match self.__text_type:
      case "text";
        return LeafNode(None, self.__text)
      case "bold":
        return LeafNode("b", self.__text)
      case "italic":
        return LeafNode("i", self.__text)
      case "code":
        return LeafNode("code", self.__text)
      case "link":
        return LeafNode("a", self.__text, { "href": self.__url })
      case "image":
        return LeafNode("img", None, { "href": self.__url, "alt": self.__text })
      case _:
        raise Exception("unknown type")

  def __eq__(self, comp):
    return self.repr() == comp.repr()
  
  def __repr__(self):
    return f"TextNode({self.__text}, {self.__text_type}, {self.__url})"
  
def text_node_to_html_node(text_node):
  return text_node.to_html_node()