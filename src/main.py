import os
import shutil

from converter import markdown_to_html_node

def copy_files(source_dir, target_dir):
  print(f"Copying from {source_dir} to {target_dir}")
  files = os.listdir(source_dir)
  if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)
  for file in files:
    source_path = os.path.join(source_dir, file)
    target_path = os.path.join(target_dir, file)
    
    if os.path.isfile(source_path):
      print(f"Copying file {source_path} to {target_path}")
      shutil.copy(source_path, target_path)
    else:
      copy_files(source_path, target_path)

def extract_title(markdown):
  titles = list(filter(lambda l: l.startswith("# "), markdown.split("\n")))
  if len(titles) == 0:
    raise Exception("no title")
  elif len(titles) > 1:
    raise Exception("multiple titles")
  return titles[0].lstrip("# ")

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  with open(from_path) as from_file:
    with open(template_path) as template_file:
      markdown = from_file.read()
      template = template_file.read()
      
      title = extract_title(markdown)
      html = "".join(map(lambda n: n.to_html(), markdown_to_html_node(markdown)))
      
      print(html)
      
      index = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
      
      with open(dest_path, "w") as dest_file:
        dest_file.write(index)

def generate_pages_recursive(source_dir, target_dir):
  print(f"Generating html from {source_dir} to {target_dir}")
  if not(os.path.exists(target_dir)):
    os.mkdir(target_dir)
  files = os.listdir(source_dir)
  
  for file in files:
    source_path = os.path.join(source_dir, file)
    
    if os.path.isfile(source_path):
      target_path = os.path.join(target_dir, file.replace(".md", ".html"))
      generate_page(source_path, os.path.join(".", "template.html"), target_path)
    else:
      target_path = os.path.join(target_dir, file)
      generate_pages_recursive(source_path, target_path)


if __name__ == "__main__":
  public_name = "public"
  static_path = os.path.join(".", "static")
  public_path = os.path.join(".", public_name)
  copy_files(static_path, public_path)
  
  generate_pages_recursive(os.path.join(".", "content"), os.path.join(".", "public"))
  # generate_page(os.path.join(".", "content", "index.md"), os.path.join(".", "template.html"), os.path.join(".", "public", "index.html"))
