import zipfile
import os
import re
from programs.utility import move_to_dir


def extract_csv(zip_file: zipfile.ZipFile):
    match = re.search(r"\d+", zip_file.filename)
    src_filename = f"pres{match[0]}_csv/pres{match[0]}comm.csv"
    dst_filename = f"{match[0]}.csv"
    zip_file.getinfo(src_filename).filename = dst_filename
    zip_file.extract(src_filename)


def main():
    # what is the best practice for file and current directory ?
    os.chdir(".")
    path = f"{os.getcwd()}/data"
    move_to_dir(path)
    pattern = r"\d{4}\.csv"
    for filename in os.listdir(path):
        try:
            if os.path.isdir(filename):
                raise TypeError("Folder detected, moving on")
            with zipfile.ZipFile(filename, "r") as zip_file:
                extract_csv(zip_file)
                zip_file.close()
                os.remove(filename)
        except zipfile.BadZipFile:
            if re.match(pattern, filename):
                pass
            else:
                print(
                    f"The file '{filename}' has unexpected format, processing with deletion"
                )
                os.remove(filename)
        except TypeError as e:
            print(e)


if __name__ == "__main__":
    main()
