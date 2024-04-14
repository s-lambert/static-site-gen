from htmlnode import HtmlNode

class LeafNode(HtmlNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
  
  def to_html(self):
    if self._HtmlNode__value == None:
      raise ValueError("leaf node requires a value")
    return super().to_html()