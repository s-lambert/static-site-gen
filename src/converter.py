import re

from htmlnode import HtmlNode
from textnode import TextNode


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
    
    split_nodes = []
    for i in range(0, len(parts)):
      # If it's odd, then it's a link
      if i % 2 == 1:
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