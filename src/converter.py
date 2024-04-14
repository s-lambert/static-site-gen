from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
    if not(isinstance(old_node, TextNode)):
      new_nodes.append(old_node)
      continue
    
    html_node = old_node.to_html_node()
    text = html_node.to_html()
    parts = text.split(delimiter)
    if len(parts) == 1:
      new_nodes.append(old_node)
      continue
    
    split_nodes = []
    for i in range(0, len(parts)):
      # If it's odd, then it's a delimited text node
      if i % 2 == 1:
        split_nodes.append(TextNode(parts[i], text_type))
      # If it's even, then it's just regular text
      elif i % 2 == 0:
        split_nodes.append(TextNode(parts[i], "text"))
    new_nodes += split_nodes
  return new_nodes