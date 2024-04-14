class HtmlNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.__tag = tag
    self.__value = value
    self.__children = children
    self.__props = props
    
  def to_html(self):
    if self.__tag == None:
      return self.__value

    content = ""
    if self.__children != None:
      content = "".join(map(lambda c: c.to_html(), self.__children))
    elif self.__value != None:
      content = self.__value

    return f"<{self.__tag}{self.props_to_html()}>{content}</{self.__tag}>"
  
  def props_to_html(self):
    prop_string = ""
    if self.__props != None:
      for k in self.__props:
        prop_string += f" {k}=\"{self.__props[k]}\""
    return prop_string
  
  def __eq__(self, comp):
    if comp == None:
      return False
    return self.__repr__() == comp.__repr__()
  
  def __repr__(self):
    return self.to_html()