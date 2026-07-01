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


class PDF(FPDF):
    def __init__(self, **kwargs):
        self.page_starts_custom = kwargs.get("page_starts", 1)
        self.font_color_custom = kwargs.get("font_color", [0, 0, 0])
        self.font_align_custom = kwargs.get("font_align", 'C')
        self.font_position_custom = kwargs.get("font_position", 15)
        self.font_style_custom = kwargs.get("font_style", "Times")
        self.font_size_custom = int(kwargs.get("font_size", 8))
        self.font_b_i_u = kwargs.get("font_b_i_u", '')

        super().__init__()

    def footer(self):
        self.set_y(-self.font_position_custom)
        self.set_text_color(self.font_color_custom[0], self.font_color_custom[1], self.font_color_custom[2])
        self.set_font(self.font_style_custom, self.font_b_i_u, self.font_size_custom)
        self.cell(0, 10, 'Page ' + str(self.page_starts_custom + self.page_no() - 1), 0, 0, self.font_align_custom)


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

        #  grayscale settings:-
        self.page_from_grayscale = self.pdf_settings.get("page_from_grayscale", "")
        self.page_to_grayscale = self.pdf_settings.get("page_to_grayscale", "")
        self.scale_type = self.pdf_settings.get("scale_type", "")
        if self.scale_type not in ["", None]:
            self.range_list = self.scale_pages_start_end()
        else:
            self.range_list = []

        #  margin settings:-
        self.h_value = self.convert_in_unit(self.pdf_settings.get("h_value", 0))
        self.v_value = self.convert_in_unit(self.pdf_settings.get("v_value", 0))

        self.ask_for_export = self.pdf_settings.get("ask_for_export", False)
        self.export_file_name = self.pdf_settings.get("export_file_name", f"jpeg2pdf_export_on_{str(int(datetime.datetime.now().timestamp()))}")

        #  page number settings:
        self.show_page_no = self.pdf_settings.get("show_page_no", False)
        self.page_starts = self.pdf_settings.get("page_starts", 1)
        self.font_color = self.pdf_settings.get("font_color", [0, 0, 0])
        self.font_align = self.pdf_settings.get("font_align", "C")
        self.font_position = self.convert_in_unit(self.pdf_settings.get("font_position", 15))
        self.font_style = self.pdf_settings.get("font_style", 'Times')
        self.font_size = self.pdf_settings.get("font_size", 8)
        self.font_b_i_u = f'{self.pdf_settings.get("bold", "")}{self.pdf_settings.get("italic", "")}' \
                          f'{self.pdf_settings.get("underline", "")}'

        #  page layout and magnification:-
        self.magnification = self.pdf_settings.get("magnification", 'default')
        self.layout = self.pdf_settings.get("layout", 'continuous')

        # page margins:-
        self.margin_l = self.convert_in_unit(self.pdf_settings.get("l_margin", 0.00))
        self.margin_r = self.convert_in_unit(self.pdf_settings.get("r_margin", 0.00))
        self.margin_t = self.convert_in_unit(self.pdf_settings.get("t_margin", 0.00))
        self.margin_b = self.convert_in_unit(self.pdf_settings.get("b_margin", 0.00))

        # DPI
        self.dpi = self.pdf_settings.get("dpi", 0.00)
        self.auto_resolution = self.pdf_settings.get("auto_resolution", True)

    def convert_in_unit(self, input_value):
        converted_value = 0
        if self.unit == "mm":
            converted_value = input_value
        elif self.unit == "cm":
            converted_value = input_value * 10
        elif self.unit == "in":
            converted_value = input_value * 25.4
        elif self.unit == "pt":
            converted_value = input_value * 0.352778

        return converted_value

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
            self.set_layout(pdf)
            if message:
                status = {"status": False, "message": message}
            else:
                if self.ask_for_export:
                    export_pdf_title = f"{self.export_file_name}"
                else:
                    export_pdf_title = f"jpeg2pdf_export_on_{str(int(datetime.datetime.now().timestamp()))}"
                self.output_path = f"{self.download_path}{export_pdf_title}.pdf"
                pdf.output(self.output_path)
                status = {"status": True, "title": export_pdf_title, "file_path": self.download_path,
                          "play_path": self.output_path, "message": ""}
            return status
        except Exception as e:
            return {"status": False, "message": str(e)}

    def set_layout(self, pdf):
        pdf.set_display_mode(self.magnification, self.layout)

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
            message = "Creation date format is Invalid, Please enter valid date format. for eg. 2021-01-25"

        return message

    def scale_pages_start_end(self):
        total_length = len(self.selected_list)
        if self.page_from_grayscale == "start" and self.page_to_grayscale == "end":
            start = 1
            end = total_length
        elif self.page_from_grayscale == "start" and self.page_to_grayscale != "end":
            start = 1
            end = int(self.page_to_grayscale)
        elif self.page_from_grayscale != "start" and self.page_to_grayscale == "end":
            start = int(self.page_from_grayscale)
            end = total_length
        else:
            start = int(self.page_from_grayscale)
            end = int(self.page_to_grayscale)

        range_list = list(range(start, end+1))
        return range_list

    def scale_pages(self, cover, index):
        pil_obj = cover
        if self.range_list:
            if index in self.range_list:
                pil_obj = cover.convert(self.scale_type)
        return pil_obj

    def auto_orientation_auto_page_size(self):
        if self.show_page_no:
            context = dict()
            context["page_starts"] = self.page_starts
            context["font_color"] = self.font_color
            context["font_position"] = self.font_position
            context["font_style"] = self.font_style
            context["font_align"] = self.font_align
            context["font_size"] = self.font_size
            context["font_b_i_u"] = self.font_b_i_u
            pdf = PDF(**context)
        else:
            pdf = FPDF(unit="mm")

        # no dpi option
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page(format=(width + self.margin_r, height + self.margin_b))
            width = width - self.h_value
            height = height - self.v_value
            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_l, height-self.margin_t)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fixed_page_format(self):
        # no margin bottom

        pdf = FPDF(unit="mm")
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(self.page_format, "A4")
            orientation = 'P' if width < height else 'L'
            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            pdf.add_page(format=self.page_format, orientation=orientation)
            if not self.auto_resolution:
                width = self.dpi
            else:
                width = width - self.h_value
            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fit_page_view(self):

        #  no dpi will be used!
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = Auto_size.get(page_format, "A4")
            orientation = 'P' if width < height else 'L'
            pdf.add_page(format=page_format, orientation=orientation)

            width = pdf_size.get(orientation).get("w") - self.h_value
            height = pdf_size.get(orientation).get("h") - self.v_value

            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2, height - self.margin_b*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fix_page_view(self):

        # margin bottom will not used.

        pdf = FPDF(unit="mm", orientation=self.orientation, format=self.page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            pdf.add_page(format=self.page_format, orientation=self.orientation)
            pdf_size = Auto_size.get(self.page_format, "A4")
            if not self.auto_resolution:
                width = self.dpi - self.h_value
            else:
                width = pdf_size.get(self.orientation).get("w") - self.h_value
            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fit_page_view(self):

        #  no dpi will be used!

        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", orientation=self.orientation, format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            pdf_size = Auto_size.get(page_format, "A4")
            pdf.add_page(orientation=self.orientation, format=page_format)

            width = pdf_size.get(self.orientation).get("w") - self.h_value
            height = pdf_size.get(self.orientation).get("h") - self.v_value

            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2, height - self.margin_b*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_auto_page_size(self):

        # margin bottom will not used.
        page_format = "A4"
        pdf = FPDF(unit="mm", orientation=self.orientation, format=page_format)
        progress_dict = {"total": len(self.selected_list), "progress": 1}

        for index, imageFile in enumerate(self.selected_list, 1):
            progress_dict["progress"] = index
            cover = Image.open(imageFile)
            cover = self.scale_pages(cover, index)
            pdf.add_page(format=page_format, orientation=self.orientation)
            pdf_size = Auto_size.get(page_format, "A4")
            if not self.auto_resolution:
                width = self.dpi - self.h_value
            else:
                width = pdf_size.get(self.orientation).get("w") - self.h_value
            pdf.image(cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r * 2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf
