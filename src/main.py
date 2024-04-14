import os
import shutil

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
  

if __name__ == "__main__":
  public_name = "public"
  static_path = os.path.join(".", "static")
  public_path = os.path.join(".", public_name)
  copy_files(static_path, public_path)
