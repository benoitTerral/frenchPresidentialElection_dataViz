import pickle
import os
import matplotlib.pyplot as plt
import geopandas as gpd
from PIL import Image, ImageDraw
import io
from pdf_library.my_pdf import My_PDF
import re


def generate_departement_map(code):
    image = Image.new("RGB", (800, 800), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    departments_gdf = gpd.read_file("./utilities/departement.geojson")
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
    return pil_image


def generate_departement_graph(names, dep_data):
    plt.figure(figsize=(16, 6))
    plt.bar(names, dep_data)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    pil_image = Image.open(buf)
    plt.close()
    return pil_image


def add_front_page(pdf, year):
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    text = f"Results of the French Election {year}"
    text_width = pdf.get_string_width(text)
    pdf_x_centered = (pdf.w - text_width) / 2
    pdf.cell(0, 10, text, ln=True, align="C")
    pdf.ln(10)
    pdf.image("election_pres.jpeg", x=10, y=pdf.get_y(), w=190)


def generate_pdf(df_departement):
    regex_candidate = r"^voix(.*)"
    names = [
        re.match(regex_candidate, col).group(1)
        for col in df_departement["2022"].columns
        if re.match(regex_candidate, col)
    ]
    pdf = My_PDF("P", "mm", "Letter", 2022)
    pdf.set_auto_page_break(auto=True, margin=15)
    add_front_page(pdf, "2022")
    x = 10
    y = 50
    width = 180
    height = 70
    for i, row in df_departement["2022"].iterrows():
        dep = row["dep"]
        nomdep = row["nomdep"]
        map = generate_departement_map(dep)
        dep_data = df_departement["2022"].iloc[i][3:]
        graph = generate_departement_graph(names, dep_data)
        pdf.add_page()
        pdf.start_section(f"{dep} - {nomdep}")
        pdf.image(map, x=10, y=10, w=40)
        pdf.set_font("Times", size=20)
        pdf.cell(0, 10, f"{dep} - {nomdep}", ln=True, align="C")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.image(graph, x, y, width, height)
        table_y = y + height + 5
        pdf.set_y(table_y)
        pdf.set_font("Times", size=10)
        table_data = {
            "Candidate": names,
            "Nb of Votes": [f"{score:,}" for score in dep_data],
            "Percentage of votes": [
                f"{score / df_departement['2022'].iloc[i][2] * 100:.2f}%"
                for score in dep_data
            ],
        }
        pdf.create_table(
            table_data=table_data, title=f"Number of votes received", cell_width="even"
        )
    pdf.output("2022.pdf")


def main():
    pickle_file = "df_departement.pkl"
    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as file:
            df_departement = pickle.load(file)
            generate_pdf(df_departement)
    else:
        print("pickle file not found")


if __name__ == "__main__":
    main()
