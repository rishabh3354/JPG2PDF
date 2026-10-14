import os
from PyQt5.QtGui import QFont, QFontDatabase

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
# text size setting index -> point size
TEXT_SIZES = [10, 11, 12, 14]
DEFAULT_TEXT_SIZE = 1

_family = None


def load_app_font():
    # the bundled Noto Sans, so the app looks the same in every snap/flatpak/desktop; system font if it's missing
    global _family
    try:
        for name in sorted(os.listdir(FONT_DIR)):
            if name.lower().endswith((".ttf", ".otf")):
                families = QFontDatabase.applicationFontFamilies(
                    QFontDatabase.addApplicationFont(os.path.join(FONT_DIR, name)))
                _family = _family or (families[0] if families else None)
    except OSError:
        pass
    return _family


def app_font(size_index):
    point_size = TEXT_SIZES[size_index] if 0 <= size_index < len(TEXT_SIZES) else TEXT_SIZES[DEFAULT_TEXT_SIZE]
    font = QFont(_family) if _family else QFont()
    font.setPointSize(point_size)
    return font


def header_css(size_index):
    # the theme gives table headers a fixed pixel size; keep them in step with the chosen text size
    point_size = app_font(size_index).pointSize()
    return (f"\nQHeaderView::section, QHeaderView::section:horizontal, QHeaderView::section:vertical "
            f"{{ font-size: {point_size}pt; }}\n")
