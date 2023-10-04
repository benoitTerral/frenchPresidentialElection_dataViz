import pickle
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
from PIL import Image, ImageDraw
import io
from pdf_library.my_pdf import My_PDF
from get_city_location import generate_communes_map, check_pickle_communes_location
import warnings


def generate_departement_map(code):
    image = Image.new("RGB", (800, 800), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # do that outside of the loop
    departments_gdf = gpd.read_file(
        f"{os.path.dirname(os.path.abspath(__file__))}/../utilities/departement.geojson"
    )
    department_geometry = departments_gdf[departments_gdf["code"] == code][
        "geometry"
    ].values[0]
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    departments_gdf.plot(ax=ax, color="lightgray", linewidth=0.5)
    departments_gdf[departments_gdf["code"] == code].plot(
        ax=ax, color="blue", alpha=0.7
    )
    plt.axis("off")
    img_file = io.BytesIO()
    plt.savefig(img_file, format="PNG", dpi=100, bbox_inches="tight")
    img_file.seek(0)
    pil_image = Image.open(img_file)
    plt.close()
    return pil_image


def generate_departement_graph(names, dep_data, colormap):
    plt.figure(figsize=(16, 6))
    plt.bar(names, dep_data, color=[colormap.get(name, "gray") for name in names])
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    pil_image = Image.open(buf)
    plt.close()
    return pil_image


def add_front_page(pdf, year):
    pdf.add_page()
    pdf.set_font("helvetica", size=16)
    text = f"Results of the French Election {year}"
    # text_width = pdf.get_string_width(text)
    # pdf_x_centered = (pdf.w - text_width) / 2
    # pdf.cell(0, 10, text, ln=True, align="C")
    pdf.cell(0, 10, text, align="C")
    pdf.ln(10)
    pdf.image(
        f"{os.path.dirname(os.path.abspath(__file__))}/../assets/election_pres.jpeg",
        x=10,
        y=pdf.get_y(),
        w=190,
    )


def generate_departement_data(
    dep, nomdep, dep_data, i, color_map, df_departement, df_dep_commune, names
):
    map_header = generate_departement_map(dep)
    graph = generate_departement_graph(names, dep_data, color_map)
    departement_map = generate_communes_map(
        dep,
        nomdep,
        df_dep_commune,
        names,
        color_map,
    )
    table_data = {
        "Candidate": names,
        "Nb of Votes": [f"{score:,}" for score in dep_data],
        "Percentage of votes": [
            f"{score / df_departement.iloc[i][2] * 100:.2f}%" for score in dep_data
        ],
    }
    return map_header, graph, departement_map, table_data


def format_page(
    pdf,
    dep,
    nomdep,
    dep_data,
    names,
    df_departement,
    i,
    map,
    graph,
    departement_map,
    table_data,
):
    pdf.add_page()
    pdf.start_section(f"{dep} - {nomdep}")
    pdf.image(map, x=10, y=10, w=40)
    pdf.set_font("Times", size=20)
    pdf.cell(0, 10, f"{dep} - {nomdep}", ln=True, align="C")
    image_params = [[10, 50], [180, 70]]
    pdf.image(
        graph,
        image_params[0][0],
        image_params[0][1],
        image_params[1][0],
        image_params[1][1],
    )
    y_position = image_params[0][1] + image_params[1][1] + 5
    pdf.set_y(y_position)
    pdf.set_font("Times", size=10)
    table_data = {
        "Candidate": names,
        "Nb of Votes": [f"{score:,}" for score in dep_data],
        "Percentage of votes": [
            f"{score / df_departement.iloc[i][2] * 100:.2f}%" for score in dep_data
        ],
    }
    pdf.create_table(table_data=table_data, cell_width="even")
    # compute y + height
    pdf.add_page()
    pdf.image(departement_map, 10, 10, 160, 160)


def generate_pdf(year, df_departement, df_commune):
    names = df_departement.columns[3:]
    colormap = mpl.colormaps.get_cmap("tab20")
    color_map = {value: colormap(idx % 20) for idx, value in enumerate(names)}
    pdf = My_PDF("P", "mm", "Letter", year=year)
    pdf.set_auto_page_break(auto=True, margin=15)
    add_front_page(pdf, year)
    for i, row in df_departement.iterrows():
        dep = row["dep"]
        nomdep = row["nomdep"]
        dep_data = df_departement.iloc[i][3:]
        map, graph, departement_map, table_data = generate_departement_data(
            dep,
            nomdep,
            dep_data,
            i,
            color_map,
            df_departement,
            df_commune.loc[df_commune["nomdep"] == nomdep],
            names,
        )
        format_page(
            pdf,
            dep,
            nomdep,
            dep_data,
            names,
            df_departement,
            i,
            map,
            graph,
            departement_map,
            table_data,
        )
    pdf.output(f"{year}.pdf")


def split_election_year(df_departements, df_communes):
    for year, df_departement in df_departements.items():
        regex_candidate = r"^voix(.*)"
        df_departement.columns = df_departement.columns.to_series().replace(
            regex_candidate, r"\1", regex=True
        )
        generate_pdf(year, df_departement, df_communes[year])


def main():
    pickle_departements = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/df_departements.pkl"
    pickle_communes = f"{os.path.dirname(os.path.abspath(__file__))}/../assets/pickles/df_communes.pkl"
    if os.path.exists(pickle_departements) and os.path.exists(pickle_communes):
        with open(pickle_departements, "rb") as departements, open(
            pickle_communes, "rb"
        ) as communes:
            df_departements = pickle.load(departements)
            df_communes = pickle.load(communes)
            split_election_year(df_departements, df_communes)
    else:
        print("pickle file not found")


if __name__ == "__main__":
    # warnings.filterwarnings("ignore")
    main()
