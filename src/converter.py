import re

from htmlnode import HtmlNode
from textnode import TextNode


def markdown_to_blocks(markdown):
  lines = map(lambda l: l.strip(), markdown.split("\n"))
  blocks = []
  current_block = []
  for line in lines:
    if len(line) == 0:
      if len(current_block) != 0:
        blocks.append(current_block)
        current_block = []
      continue
    current_block.append(line)
  if len(current_block) != 0:
    blocks.append(current_block)
    current_block = []
  return blocks

def block_to_blocktype(block):
  if len(block) == 0:
    raise Exception("invalid block")
  if len(block) == 1 and re.match(r"#*\s.*", block[0]):
    return "heading"
  if len(block) >= 3 and block[0].startswith("```") and block[-1].endswith("```"):
    return "code"
  if all(map(lambda s: s.startswith(">"), block)):
    return "quote"
  if all(map(lambda s: s[0] == "*" or s[0] == "-", block)):
    return "unordered_list"
  
  is_ordered_list = True
  ordinal = 0
  for line in block:
    matches = re.match(r"([0-9]*)\..*", line)
    if matches == None:
      is_ordered_list = False
      break
    try:
      value = int(matches[1])
      ordinal += 1
      if value != ordinal:
        print("ordinal mismatch")
        is_ordered_list = False
        break
    except:
      print("exception")
      is_ordered_list = False
      break
  
  if is_ordered_list:
    return "ordered_list"
  
  return "paragraph"

def text_to_textnodes(text):
  return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, "text")], "`", "code"), "**", "bold"), "*", "italic")))

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

def split_nodes_image(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if not(isinstance(old_node, TextNode)):
      new_nodes.append(old_node)
      continue
    
    html_node = old_node.to_html_node()
    text = html_node.to_html()
    images = extract_markdown_images(text)
    parts = split_many(lambda i: f"![{i[0]}]({i[1]})", images, text)
    if len(parts) == 1:
      new_nodes.append(old_node)
      continue
    
    split_nodes = []
    for i in range(0, len(parts)):
      # If it's odd, then it's an image
      if i % 2 == 1:
        split_nodes.append(TextNode(parts[i][0], "image", parts[i][1]))
      elif i % 2 == 0:
        split_nodes.append(TextNode(parts[i], "text"))
    new_nodes += split_nodes
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if not(isinstance(old_node, TextNode)):
      new_nodes.append(old_node)
      continue
    
    html_node = old_node.to_html_node()
    text = html_node.to_html()
    images = extract_markdown_links(text)
    parts = split_many(lambda i: f"[{i[0]}]({i[1]})", images, text)
    if len(parts) == 1:
      new_nodes.append(old_node)
      continue

    print(parts)
    split_nodes = []
    for i in range(0, len(parts)):
      # If it's odd, then it's a link
      if i % 2 == 1:
        print(parts[i])
        split_nodes.append(TextNode(parts[i][0], "link", parts[i][1]))
      elif i % 2 == 0:
        split_nodes.append(TextNode(parts[i], "text"))
    new_nodes += split_nodes
  return new_nodes

def split_many(formatter, strs, text):
  parts = []
  to_split = text
  for s in strs:
    split_on = formatter(s)
    after_split = to_split.split(split_on)
    parts += after_split[:-1]
    parts += [s]
    to_split = after_split[-1]
  if to_split != "":
    parts += [to_split]
  return parts

def extract_markdown_images(text):
  image_regex = r"!\[(.*?)\]\((.*?)\)"
  return find_pairs(image_regex, text)

def extract_markdown_links(text):
  link_regex = r"\[(.*?)\]\((.*?)\)"
  return find_pairs(link_regex, text)

def find_pairs(regex, text):
  matches = re.findall(regex, text)
  pairs = []
  for pair in matches:
    pairs.append((pair[0], pair[1]))
  return pairs

def block_to_heading(block):
  return HtmlNode(
    f"h{block[0].count("#")}",
    block[0].lstrip("# ")
  )

def block_to_code(block):
  return HtmlNode(
    "pre",
    None,
    [
      HtmlNode(
        "code",
        "\n".join(block[1:-1])
      )
    ]
  )

def block_to_quote(block):
  return HtmlNode(
    "blockquote",
    "\n".join(block)
  )

def block_to_unordered_list(block):
  return HtmlNode(
    "ul",
    None,
    map(lambda l: HtmlNode("li", l.lstrip("* ")), block)
  )

def block_to_ordered_list(block):
  return HtmlNode(
    "ol",
    None,
    map(lambda l: HtmlNode("li", l.lstrip("0123456789. ")), block)
  )

def block_to_paragraph(block):
  return HtmlNode(
    'p',
    None,
    sum(map(lambda l: text_to_textnodes(l + "\n"), block), []),
    None
  )

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  print("BLOCKS", blocks)
  nodes = []
  for block in blocks:
    blocktype = block_to_blocktype(block)
    match blocktype:
      case "heading":
        nodes.append(block_to_heading(block))
      case "code":
        nodes.append(block_to_code(block))
      case "quote":
        nodes.append(block_to_quote(block))
      case "unordered_list":
        nodes.append(block_to_unordered_list(block))
      case "ordered_list":
        nodes.append(block_to_ordered_list(block))
      case "paragraph":
        nodes.append(block_to_paragraph(block))
      case _:
        raise Exception("unknown blocktype")
  
  return nodes