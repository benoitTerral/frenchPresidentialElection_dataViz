from pdf_library.create_table_fpdf2 import PDF


class My_PDF(PDF):
    def __init__(self, orientation="P", unit="mm", format="Letter", year=None):
        super().__init__(orientation, unit, format)
        self.year = year

    def header(self):
        self.set_font("helvetica", "B", 10)
        title = f"French presidential election {self.year}"
        title_w = self.get_string_width(title) + 3
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)
        self.set_text_color(0, 80, 180)
        self.cell(
            title_w,
            10,
            f"French presidential election {self.year}",
            border=False,
            ln=1,
            align="C",
        )
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
