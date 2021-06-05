from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from fpdf import FPDF

A3 = {'P': {'w': 297, 'h': 420}, 'L': {'w': 420, 'h': 297}}
A4 = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
A5 = {'P': {'w': 148, 'h': 210}, 'L': {'w': 210, 'h': 148}}
Letter = {'P': {'w': 216, 'h': 279}, 'L': {'w': 279, 'h': 216}}
Auto_size = {"A3": A3, "A4": A4, "A5": A5, "Letter": Letter}
orientation_dict = {"Landscape": "L", "Portrait": "P"}


class ConvertToPdfThread(QtCore.QThread):
    finish = pyqtSignal(dict)

    def __init__(self, selected_list, download_path, pdf_settings, parent=None):
        super(ConvertToPdfThread, self).__init__(parent)
        self.selected_list = selected_list
        self.download_path = download_path
        self.pdf_settings = pdf_settings

        #  pdf attributes
        self.title = self.pdf_settings.get("title", "jpf2pdf_output_file")
        if self.pdf_settings.get("orientation", "Auto") in ["Landscape", "Portrait"]:
            self.orientation = orientation_dict.get(self.pdf_settings.get("orientation", "Landscape"))
        else:
            self.orientation = self.pdf_settings.get("orientation", "Auto")
        self.page_format = self.pdf_settings.get("page_format", "Auto")
        self.unit = self.pdf_settings.get("unit", "mm")

    def run(self):
        response = self.convert_to_pdf()
        self.finish.emit(response)

    def convert_to_pdf(self):
        status = {"status": False, "message": ""}
        try:
            # Auto / Auto
            if self.orientation == "Auto" and self.page_format == "Auto":
                pdf = self.auto_orientation_auto_page_size()
                name = f"{self.download_path}{self.title}.pdf"
                pdf.output(name)
                status = {"status": True, "message": ""}
            else:
                # Auto / A3, A4 .. etc
                if self.orientation == "Auto":
                    if self.page_format in ["A3", "A4", "A5", "Letter"]:
                        pdf = self.auto_orientation_fixed_page_format()
                        name = f"{self.download_path}{self.title}.pdf"
                        pdf.output(name)
                        status = {"status": True, "message": ""}

                    elif self.page_format in ["A3 (Fit view)", "A4 (Fit view)", "A5 (Fit view)", "Letter (Fit view)"]:
                        pdf = self.auto_orientation_fit_page_view()
                        name = f"{self.download_path}{self.title}.pdf"
                        pdf.output(name)
                        status = {"status": True, "message": ""}

                elif self.orientation in ["L", "P"]:
                    if self.page_format in ["A3", "A4", "A5", "Letter"]:
                        pdf = self.fix_orientation_fix_page_view()
                        name = f"{self.download_path}{self.title}.pdf"
                        pdf.output(name)
                        status = {"status": True, "message": ""}

                    elif self.page_format in ["A3 (Fit view)", "A4 (Fit view)", "A5 (Fit view)", "Letter (Fit view)"]:
                        pdf = self.fix_orientation_fit_page_view()
                        name = f"{self.download_path}{self.title}.pdf"
                        pdf.output(name)
                        status = {"status": True, "message": ""}

                    elif self.page_format == "Auto":
                        pdf = self.fix_orientation_auto_page_size()
                        name = f"{self.download_path}{self.title}.pdf"
                        pdf.output(name)
                        status = {"status": True, "message": ""}

            return status
        except Exception as e:
            return {"status": False, "message": str(e)}

    def auto_orientation_auto_page_size(self):
        pdf = FPDF(unit=self.unit)

        for imageFile in self.selected_list:
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page(format=(width, height))
            pdf.image(imageFile, 0, 0, width, height)

        return pdf

    def auto_orientation_fixed_page_format(self):
        pdf = FPDF(unit=self.unit)

        for imageFile in self.selected_list:
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(self.page_format, "A4")
            orientation = 'P' if width < height else 'L'
            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
            pdf.add_page(orientation=orientation)
            pdf.image(imageFile, 0, 0, width, height)

        return pdf

    def auto_orientation_fit_page_view(self):
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit=self.unit, format=page_format)

        for imageFile in self.selected_list:
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(page_format, "A4")
            orientation = 'P' if width < height else 'L'
            pdf.add_page(orientation=orientation)
            print(width, height)
            pdf.image(imageFile, 0, 0, pdf_size.get(orientation).get("w"), pdf_size.get(orientation).get("h"))

        return pdf

    def fix_orientation_fix_page_view(self):
        pdf = FPDF(unit=self.unit, orientation=self.orientation, format=self.page_format)
        for imageFile in self.selected_list:
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page()
            pdf.image(imageFile, 0, 0, width, height)

        return pdf

    def fix_orientation_fit_page_view(self):
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit=self.unit, orientation=self.orientation, format=page_format)

        for imageFile in self.selected_list:
            pdf_size = Auto_size.get(page_format, "A4")
            pdf.add_page()
            pdf.image(imageFile, 0, 0, pdf_size.get(self.orientation).get("w"), pdf_size.get(self.orientation).get("h"))

        return pdf

    def fix_orientation_auto_page_size(self):
        page_format = "A4"
        pdf = FPDF(unit=self.unit, orientation=self.orientation, format=page_format)

        for imageFile in self.selected_list:
            pdf_size = Auto_size.get(page_format, "A4")
            pdf.add_page()
            pdf.image(imageFile, 0, 0, pdf_size.get(self.orientation).get("w"), pdf_size.get(self.orientation).get("h"))

        return pdf
