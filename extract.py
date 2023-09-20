import zipfile
import os
import re


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
    if not (os.path.exists(path) and os.path.isdir(path)):
        raise Exception("data folder not found")
    os.chdir(path)
    for filename in os.listdir(path):
        try:
            if os.path.isdir(filename):
                raise TypeError("Folder detected, moving on")
            with zipfile.ZipFile(filename, "r") as zip_file:
                extract_csv(zip_file)
                zip_file.close()
                os.remove(filename)
        except zipfile.BadZipFile:
            print(f"The file '{filename}' is not a zip file.")
        except TypeError as e:
            print(e)


if __name__ == "__main__":
    main()
