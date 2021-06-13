import datetime
import pikepdf
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from fpdf import FPDF

A3 = {'P': {'w': 297, 'h': 420}, 'L': {'w': 420, 'h': 297}}
A4 = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
A5 = {'P': {'w': 149, 'h': 210}, 'L': {'w': 210, 'h': 149}}
Letter = {'P': {'w': 216, 'h': 280}, 'L': {'w': 280, 'h': 216}}
Auto_size = {"A3": A3, "A4": A4, "A5": A5, "Letter": Letter}
orientation_dict = {"Landscape": "L", "Portrait": "P"}


class ConvertToPdfThread(QtCore.QThread):
    finish = pyqtSignal(dict)
    progress = pyqtSignal(dict)
    kill = pyqtSignal()

    def __init__(self, selected_list, download_path, pdf_settings, parent=None):
        super(ConvertToPdfThread, self).__init__(parent)
        self.selected_list = selected_list
        self.download_path = download_path
        self.pdf_settings = pdf_settings
        self.output_path = ""

        self.is_killed = False

        #  pdf attributes
        if self.pdf_settings.get("orientation", "Auto") in ["Landscape", "Portrait"]:
            self.orientation = orientation_dict.get(self.pdf_settings.get("orientation", "Landscape"))
        else:
            self.orientation = self.pdf_settings.get("orientation", "Auto")
        self.page_format = self.pdf_settings.get("page_format", "Auto")
        self.unit = self.pdf_settings.get("unit", "mm")

        self.title = self.pdf_settings.get("title", "jpf2pdf_output")
        self.subject = self.pdf_settings.get("subject", "")
        self.author = self.pdf_settings.get("author", "")
        self.password = self.pdf_settings.get("password")

        #  Advance meta-data settings:-
        self.keywords = self.pdf_settings.get("keywords", "")
        self.producer = self.pdf_settings.get("producer", "")
        self.creator = self.pdf_settings.get("creator", "")
        self.created_on = self.pdf_settings.get("created_on", "")

        #  Rotate settings:-
        self.page_from = self.pdf_settings.get("page_from", "")
        self.page_to = self.pdf_settings.get("page_to", "")
        self.rotation_angle = self.pdf_settings.get("rotation_angle", "")

        #  margin settings:-
        self.h_value = self.pdf_settings.get("h_value", 0)
        self.v_value = self.pdf_settings.get("v_value", 0)

        if self.unit == "cm":
            self.h_value = self.pdf_settings.get("h_value", 0) * 10
            self.v_value = self.pdf_settings.get("v_value", 0) * 10
        elif self.unit == "in":
            self.h_value = self.pdf_settings.get("h_value", 0) * 25.4
            self.v_value = self.pdf_settings.get("v_value", 0) * 25.4
        elif self.unit == "pt":
            self.h_value = self.pdf_settings.get("h_value", 0) * 0.352778
            self.v_value = self.pdf_settings.get("v_value", 0) * 0.352778

        self.ask_for_export = self.pdf_settings.get("ask_for_export", False)
        self.export_file_name = self.pdf_settings.get("export_file_name", f"jpf2pdf_export_on_{str(datetime.datetime.now())}")

    def run(self):
        response = self.convert_to_pdf()
        if not self.is_killed:
            if self.password not in [None, ""]:
                self.set_password()
            if self.rotation_angle not in [None, ""]:
                self.rotate_pages()
            self.finish.emit(response)

    def rotate_pages(self):
        with pikepdf.open(self.output_path, allow_overwriting_input=True) as pdf:
            total_length = len(pdf.pages)
            if self.page_from == "start" and self.page_to == "end":
                start = 0
                end = total_length
            elif self.page_from == "start" and self.page_to != "end":
                start = 0
                end = int(self.page_to)
            elif self.page_from != "start" and self.page_to == "end":
                start = int(self.page_from) - 1
                end = total_length
            else:
                start = int(self.page_from) - 1
                end = int(self.page_to)

            for p_no in range(start, end):
                try:
                    page = pdf.pages[p_no]
                    page.Rotate = int(self.rotation_angle)
                except Exception as e:
                    continue
            pdf.save(self.output_path)

    def set_password(self):
        with pikepdf.open(self.output_path, allow_overwriting_input=True) as pdf:
            no_extracting = pikepdf.Permissions(extract=False)
            pdf.save(self.output_path, encryption=pikepdf.Encryption(
                user=self.password, owner=self.password, allow=no_extracting
            ))

    def convert_to_pdf(self):
        pdf = None
        try:
            # Auto / Auto
            if self.orientation == "Auto" and self.page_format == "Auto":
                pdf = self.auto_orientation_auto_page_size()
            else:
                # Auto / A3, A4 .. etc
                if self.orientation == "Auto":
                    if self.page_format in ["A3", "A4", "A5", "Letter"]:
                        pdf = self.auto_orientation_fixed_page_format()
                    elif self.page_format in ["A3 (Fit view)", "A4 (Fit view)", "A5 (Fit view)", "Letter (Fit view)"]:
                        pdf = self.auto_orientation_fit_page_view()

                elif self.orientation in ["L", "P"]:
                    if self.page_format in ["A3", "A4", "A5", "Letter"]:
                        pdf = self.fix_orientation_fix_page_view()

                    elif self.page_format in ["A3 (Fit view)", "A4 (Fit view)", "A5 (Fit view)", "Letter (Fit view)"]:
                        pdf = self.fix_orientation_fit_page_view()

                    elif self.page_format == "Auto":
                        pdf = self.fix_orientation_auto_page_size()

            message = self.set_meta_data(pdf)
            if message:
                status = {"status": False, "message": message}
            else:
                if self.ask_for_export:
                    export_pdf_title = f"{self.export_file_name}"
                else:
                    export_pdf_title = f"jpf2pdf_export_on_{str(datetime.datetime.now())}"
                self.output_path = f"{self.download_path}{export_pdf_title}.pdf"
                pdf.output(self.output_path)
                status = {"status": True, "title": export_pdf_title, "file_path": self.download_path,
                          "play_path": self.output_path, "message": ""}
            return status
        except Exception as e:
            return {"status": False, "message": str(e)}

    def set_meta_data(self, pdf):
        message = None
        pdf.set_title(self.title)
        pdf.set_subject(self.subject)
        pdf.set_author(self.author)
        pdf.set_keywords(self.keywords)
        pdf.set_creator(self.creator)
        pdf.set_producer(self.producer)
        try:
            if self.created_on:
                date_obj = datetime.datetime.strptime(self.created_on, "%Y-%m-%d")
                date_obj = datetime.datetime.now().replace(day=date_obj.day, month=date_obj.month, year=date_obj.year)
                pdf.set_creation_date(date_obj)
        except Exception as e:
            message = "Creation date format is Invalid, Please enter valid date format. for eg.(2021-01-25)"

        return message

    def auto_orientation_auto_page_size(self):
        pdf = FPDF(unit="mm")
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page(format=(width, height))
            width = width - self.h_value
            height = height - self.v_value
            pdf.image(imageFile, self.h_value, self.h_value, width, height)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fixed_page_format(self):
        pdf = FPDF(unit="mm")
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(self.page_format, "A4")
            orientation = 'P' if width < height else 'L'
            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
            pdf.add_page(orientation=orientation)
            width = width - self.h_value
            height = height - self.v_value
            pdf.image(imageFile, self.h_value, self.v_value, width, height)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fit_page_view(self):
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(page_format, "A4")
            orientation = 'P' if width < height else 'L'
            pdf.add_page(orientation=orientation)
            print(width, height)
            pdf.image(imageFile, self.h_value, self.v_value, pdf_size.get(orientation).get("w")
                      - self.h_value, pdf_size.get(orientation).get("h") - self.v_value)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fix_page_view(self):
        pdf = FPDF(unit="mm", orientation=self.orientation, format=self.page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page()
            width = width - self.h_value
            height = height - self.v_value
            pdf.image(imageFile, self.h_value, self.v_value, width, height)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fit_page_view(self):
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", orientation=self.orientation, format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            pdf_size = Auto_size.get(page_format, "A4")
            pdf.add_page()
            pdf.image(imageFile, self.h_value, self.v_value, pdf_size.get(self.orientation).get("w") -
                      self.h_value, pdf_size.get(self.orientation).get("h") - self.v_value)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_auto_page_size(self):
        page_format = "A4"
        pdf = FPDF(unit="mm", orientation=self.orientation, format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            pdf_size = Auto_size.get(page_format, "A4")
            pdf.add_page()
            pdf.image(imageFile, self.h_value, self.v_value, pdf_size.get(self.orientation).get("w")
                      - self.h_value, pdf_size.get(self.orientation).get("h") - self.v_value)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf
