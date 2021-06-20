THEME_DICT = {"dark": "dark.qss", "light": "light.qss"}


def set_theme(self, theme):
    from jpg2pdf import THEME_PATH
    self.setStyleSheet(open(THEME_PATH + THEME_DICT.get(theme, "dark"), 'r').read())


def popup_theme(self):
    if self.theme == "dark":
        style_sheet = "background-color:rgb(48,48,48);color:white;"
    elif self.theme == "light":
        style_sheet = "background-color:rgb(201,205,208);color:black;"
    else:
        style_sheet = "background-color:rgb(250,250,250);color:black;"

    return style_sheet
