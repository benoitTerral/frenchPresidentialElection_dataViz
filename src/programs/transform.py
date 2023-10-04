import os
import re
from utility import move_to_dir
import pandas as pd
import pickle


def main():
    pattern = r"(\d{4})\.csv"
    path = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/data"
    move_to_dir(path)
    dataframes = {}
    for filename in os.listdir(path):
        match = re.match(pattern, filename)
        if match:
            try:
                dataframes[match.group(1)] = pd.read_csv(filename, low_memory=False)
            except pd.errors.ParserWarning as e:
                print(e)
    for key, value in dataframes.items():
        print(f"Key: {key}, Value: {type(value)}")
    pickle_file = "df_communes.pkl"
    destination_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../assets", "pickles"
    )
    os.makedirs(destination_dir, exist_ok=True)
    os.chdir(destination_dir)
    with open(pickle_file, "wb") as file:
        pickle.dump(dataframes, file)
        print(f"Dataframes saved as {pickle_file}")


if __name__ == "__main__":
    main()
