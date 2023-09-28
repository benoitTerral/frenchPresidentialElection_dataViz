import os


def move_to_dir(path):
    try:
        os.chdir(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"{path} directory not found: {e}")
