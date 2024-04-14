from textnode import TextNode

if __name__ == "__main__":
  test = TextNode("This is a text node", "bold", "https://www.boot.dev")
  print(test.repr())