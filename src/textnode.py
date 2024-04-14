class TextNode:
  def __init__(self, text, text_type, url=None):
    self.__text = text
    self.__text_type = text_type
    self.__url = url

  def __eq__(self, comp):
    return self.repr() == comp.repr()
  
  def repr(self):
    return f"TextNode({self.__text}, {self.__text_type}, {self.__url})"