from htmlnode import HtmlNode


class ParentNode(HtmlNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)
  
  