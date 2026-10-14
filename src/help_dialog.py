from PyQt5.QtWidgets import QDialog, QTextBrowser, QPushButton, QVBoxLayout, QHBoxLayout

HELP_HTML = """
<h2>How to use JPEG2PDF</h2>

<h3>1. Add images</h3>
<p>Use the <b>Add images</b> or <b>Add a folder of images</b> buttons at the top, or drag images or folders into the
window. New images are ticked automatically.</p>

<h3>2. Put them in order</h3>
<ul>
<li><b>Sort by</b> sorts by name, date changed, file size or the date a photo was taken.</li>
<li>Drag images in the list, or use <b>Move up</b> / <b>Move down</b>. Right-click for <b>Move to top/bottom</b>.</li>
<li>Click an image to see it on the right.</li>
</ul>

<h3>3. Fix single images</h3>
<p>Under the preview: <b>rotate left/right</b>, <b>crop</b>, or <b>remove</b> the image. These change only the PDF,
never your image files. Select several images (Ctrl- or Shift-click) to rotate them together.</p>

<h3>4. Choose which images to use</h3>
<p>Only <b>ticked</b> images go into the PDF. Click the <b>&#10003;</b> column header to tick or untick all.
If nothing is ticked, all images are used.</p>

<h3>5. Page settings</h3>
<ul>
<li><b>Orientation</b> and <b>Page size</b>: "Auto" makes every page fit its image. Choose A4, Letter, Legal or a
custom size for printing.</li>
<li><b>Advanced PDF settings</b>: make the PDF smaller, put several images on one page, clean up scans, page numbers,
make a separate PDF for each image, searchable text, and more. Save your favourite settings as a <b>preset</b>.</li>
</ul>

<h3>6. Create the PDF</h3>
<p><b>Preview PDF</b> shows the first 10 pages without saving. <b>Create PDF</b> saves it in the folder shown next to
<b>Save to...</b> (you can choose any folder, including USB drives).</p>

<h3>Keyboard shortcuts</h3>
<table cellpadding="3">
<tr><td><b>Ctrl+O</b></td><td>Add images</td></tr>
<tr><td><b>Ctrl+Shift+O</b></td><td>Add a folder of images</td></tr>
<tr><td><b>Ctrl+T</b></td><td>Tick or untick all images</td></tr>
<tr><td><b>Delete</b></td><td>Remove the highlighted images from the list</td></tr>
<tr><td><b>Ctrl+R / Ctrl+L</b></td><td>Rotate right / left</td></tr>
<tr><td><b>Ctrl+Z</b></td><td>Undo the last change to the list</td></tr>
<tr><td><b>Ctrl+P</b></td><td>Preview PDF</td></tr>
<tr><td><b>Ctrl+Enter</b></td><td>Create PDF</td></tr>
<tr><td><b>F1</b></td><td>This help</td></tr>
</table>
"""


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setWindowTitle("JPEG2PDF PRO | Help")
        self.resize(640, 720)
        text = QTextBrowser(self)
        text.setHtml(HELP_HTML)
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(close_button)
        layout = QVBoxLayout(self)
        layout.addWidget(text)
        layout.addLayout(buttons)
