from geopy.geocoders import Nominatim
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from unidecode import unidecode
from PIL import Image, ImageDraw
import io
import matplotlib.patches as mpatches


def add_zero(code, expected_length):
    """Only one 0 missing maximum"""
    if len(str(code)) < expected_length:
        return "0" + str(code)
    else:
        return str(code)


def check_pickle_communes_location():
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/communes_location.pkl"
    if os.path.exists(file_path):
        pass
    else:
        df = pd.read_csv(
            f"{os.path.dirname(os.path.abspath(__file__))}/../assets/communes-departement-region.csv"
        )
        df["code_commune_INSEE"] = df["code_commune_INSEE"].apply(
            add_zero, expected_length=5
        )
        df["code_departement"] = df["code_departement"].apply(
            add_zero, expected_length=2
        )
        with open(file_path, "wb") as pickle_file:
            pickle.dump(df, pickle_file)
    return file_path


def generate_communes_map(dep, nomdep, df_communes, names, color_map):
    image = Image.new("RGB", (800, 800), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    filtered_columns = df_communes.filter(regex="^voix(?!.*ratio)(?!.*T2)")
    df_communes["frontrunner"] = filtered_columns.idxmax(axis=1)
    df_communes["frontrunner"] = df_communes["frontrunner"].str.extract(r"^voix(.*)")
    # no need to match nom dep only dep
    nomdep = unidecode(nomdep.strip().replace(" ", "-").replace("'", "-").lower())
    department_map = gpd.read_file(
        f"{os.path.dirname(os.path.abspath(__file__))}/../assets/geojson/communes-{dep}-{nomdep}.geojson"
    )
    merged_df = pd.merge(
        department_map,
        df_communes,
        left_on="code",
        right_on="codecommune",
    )
    merged_df = merged_df[["code", "geometry", "frontrunner"]]
    ax = merged_df.plot(
        column="frontrunner",
        color=[color_map[name] for name in merged_df["frontrunner"]],
        legend=True,
    )
    legend_labels = [
        mpatches.Patch(color=color_map[value], label=value)
        for value in merged_df["frontrunner"].unique()
    ]
    ax.legend(
        handles=legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.2),
        fontsize="small",
        ncols=3,
    )
    plt.axis("off")
    img_file = io.BytesIO()
    plt.savefig(img_file, format="PNG", dpi=100, bbox_inches="tight")
    img_file.seek(0)
    pil_image = Image.open(img_file)
    plt.close()
    return pil_image
