# JPEG2PDF — Image to PDF Converter for Linux (JPG, PNG, TIFF, WebP, SVG)

**JPEG2PDF is a fast, offline image-to-PDF converter for Linux.** Batch convert JPG, PNG, BMP, GIF, TIFF, SVG and WebP images into high-quality PDF documents — with page size and margin control, custom DPI, page numbering, rotation, grayscale output and AES-256 password protection. Everything runs locally; your images never leave your computer.

**Open source (MIT), written in Python and PyQt5** — the full application source is in this repository.

<p align="center">
  <a href="https://flathub.org/apps/details/com.warlordsoftwares.jpeg2pdf"><img src="https://img.shields.io/flathub/downloads/com.warlordsoftwares.jpeg2pdf?style=for-the-badge&label=Flathub%20installs&color=4A90D9" alt="Flathub installs"></a>
  <a href="https://snapcraft.io/jpg2pdf"><img src="https://img.shields.io/snapcraft/v/jpg2pdf/latest/stable?style=for-the-badge&label=Snap&color=E95420" alt="Snap Store version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/rishabh3354/JPG2PDF?style=for-the-badge&color=2ea44f" alt="MIT licensed"></a>
  <a href="https://github.com/rishabh3354/JPG2PDF/stargazers"><img src="https://img.shields.io/github/stars/rishabh3354/JPG2PDF?style=for-the-badge&color=f5c518" alt="GitHub stars"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Ubuntu%20%7C%20Debian%20%7C%20Fedora%20%7C%20Arch-blue?style=flat-square&logo=linux&logoColor=white" alt="Runs on Ubuntu, Debian, Fedora and Arch Linux">
  <img src="https://img.shields.io/badge/Python-PyQt5-3776AB?style=flat-square&logo=python&logoColor=white" alt="Built with Python and PyQt5">
  <img src="https://img.shields.io/badge/Encryption-AES--256-success?style=flat-square" alt="AES-256 PDF encryption">
  <img src="https://img.shields.io/badge/Offline-100%25%20local-success?style=flat-square" alt="Runs entirely offline">
</p>

> **Installed 28,000+ times on Flathub.**

---

## Contents

- [Screenshots](#-screenshots)
- [Install](#-install)
- [Features](#-features)
- [Supported image formats](#-supported-image-formats)
- [Common tasks](#-common-tasks)
- [Run from source](#-run-from-source)
- [FAQ](#-faq)
- [How it compares](#-how-it-compares)
- [More apps](#-more-apps-by-warlord-softwares)

---

## 📸 Screenshots

| Dark theme | Light theme |
|---|---|
| ![JPEG2PDF main window in dark theme — image queue with dimensions, format and file size, live preview and PDF settings](https://raw.githubusercontent.com/rishabh3354/FLATPAK_JPEG2PDF/main/share/screenshots/jpeg2pdf_screenshot_1.png) | ![JPEG2PDF main window in light theme showing the same batch conversion queue](https://raw.githubusercontent.com/rishabh3354/FLATPAK_JPEG2PDF/main/share/screenshots/jpeg2pdf_screenshot_4.png) |

![JPEG2PDF app settings and advanced PDF settings — measure units, page margins, image position, DPI and page rotation](https://raw.githubusercontent.com/rishabh3354/FLATPAK_JPEG2PDF/main/share/screenshots/jpeg2pdf_screenshot_2.png)

---

## 📥 Install

<p align="center">
  <a href="https://snapcraft.io/jpg2pdf"><img src="https://snapcraft.io/static/images/badges/en/snap-store-black.svg" height="56" alt="Install JPEG2PDF from the Snap Store"></a>&nbsp;
  <a href="https://flathub.org/apps/details/com.warlordsoftwares.jpeg2pdf"><img src="https://flathub.org/assets/badges/flathub-badge-en.png" height="56" width="186" alt="Install JPEG2PDF from Flathub"></a>
</p>

### Snap

```bash
sudo snap install jpg2pdf
```

```bash
jpg2pdf
```

### Flatpak

```bash
flatpak install flathub com.warlordsoftwares.jpeg2pdf
```

```bash
flatpak run com.warlordsoftwares.jpeg2pdf
```

Works on Ubuntu, Debian, Fedora, Arch, Linux Mint, Pop!\_OS and any other distribution with Snap or Flatpak.

---

## 🌟 Features

- **Batch convert** — turn a whole folder of images into PDFs in one click.
- **One PDF or many** — merge every image into a single document, or export one PDF per image.
- **Sort and reorder** — sort by name, date modified, file size or date taken, drag images into any order, or move them to the top or bottom.
- **Ticked automatically** — new images are ready to convert; click the ✓ column header to tick or untick all.
- **Page sizes** — A4, A3, A5, Letter, Legal or any custom size, with automatic orientation.
- **Several images per page** — 2, 4, 6 or 9 per page, great for receipts and ID cards.
- **Margins and positioning** — set page margins and image placement in mm, cm, pt or inches.
- **Custom DPI** — pick the image resolution that suits print or screen.
- **Rotate and crop** — fix single images (only the PDF changes, never your files), or rotate a page range.
- **Clean up scans** — straighten tilted pages, cut off dark borders and make text clearer.
- **Smaller PDFs** — compress images, split into several PDFs, or add images to an existing PDF.
- **One PDF per image** — keeps each file's name (photo.tif → photo.pdf), including multi-page TIFFs.
- **Searchable PDFs** — OCR makes the text searchable and copyable (snap).
- **Grayscale and black-and-white** output.
- **Page numbering** with configurable fonts and styles.
- **AES-256 encryption** — password-protect the resulting PDF.
- **PDF metadata** — set title, subject and author.
- **Drag and drop** images straight into the window.
- **Live preview** with zoom before you export.
- **Presets, preview and undo** — save favourite settings, preview the PDF before saving, undo list changes (Ctrl+Z).
- **Save anywhere** — any folder, including USB drives; folders can be imported with their subfolders.
- **Built-in help and shortcuts** (F1), adjustable text size, dark and light themes.
- **Fully offline** — no upload, no file-size limit, no watermark, no ads.

---

## 🖼 Supported image formats

`JPG` · `JPEG` · `PNG` · `BMP` · `GIF` · `TIFF` · `TIF` · `SVG` · `WebP` · `HEIC` (snap)

...and other formats readable by Pillow.

---

## 🔁 Common tasks

| Task | How JPEG2PDF handles it |
|---|---|
| **Convert JPG to PDF** | Drop the images in and export — one click |
| **Convert PNG to PDF** | Same flow; transparency is flattened onto the page |
| **Merge multiple images into one PDF** | Queue them, reorder, export as a single document |
| **Convert a scanned document to PDF** | Auto orientation and DPI control for readable scans |
| **Convert TIFF to PDF** | Multi-format queue, no conversion step needed first |
| **Password protect a PDF** | Tick Password and set an AES-256 password |
| **Make a grayscale PDF** | Toggle grayscale to shrink scans and photos |
| **Add page numbers** | Enable numbering and pick the font and style |
| **Set A4 or Letter page size** | Choose the page size, or leave it on Auto |
| **Convert a whole folder** | Add a folder of images, then Create PDF |
| **One PDF per image, same file names** | Advanced settings → Split or join PDFs → Make a separate PDF for each image |
| **Several receipts on one page** | Advanced settings → Page layout → Images per page |

---

## 🛠 Run from source

The application is MIT licensed and the full source is in [`src/`](src).

```bash
git clone https://github.com/rishabh3354/JPG2PDF.git
cd JPG2PDF
```

Install PyQt5 and the Python dependencies:

```bash
sudo apt install python3-pyqt5          # Debian / Ubuntu
pip install -r req.txt                  # Pillow, fpdf2, pikepdf
```

Run it:

```bash
python3 src/jpg2pdf.py
```

### Building the snap

```bash
snapcraft
```

The snap consumes **[pyqt5-runtime-core22-lite](https://github.com/rishabh3354/pyqt5-runtime-core22-lite)** as a content snap rather than bundling PyQt5, which is what keeps the package small — [`snap/snapcraft.yaml`](snap/snapcraft.yaml) is a working reference if you are packaging a PyQt5 app the same way.

---

## ❓ FAQ

### Is JPEG2PDF free?

Yes. It is free to install from Flathub and the Snap Store, and the source is MIT licensed.

### Does it upload my images anywhere?

No. All conversion happens locally on your machine. There is no upload, no account, and no file-size limit — which matters if you are converting scanned IDs, contracts or medical records.

### Can it merge several images into one PDF?

Yes. Add all the images, reorder them however you like, and export a single PDF. You can also export one PDF per image.

### Can it password protect the PDF?

Yes, with AES-256 encryption. Set the password before exporting.

### What image formats does it support?

JPG, JPEG, PNG, BMP, GIF, TIFF, SVG and WebP, plus other formats Pillow can read.

### Can I control page size and margins?

Yes — A4, A3, A5, Letter, Legal or a custom size, with margins and image position configurable in mm, cm, pt or inches, and a custom DPI setting.

### Does it work on Wayland?

Yes. The packaged builds run under XWayland for compatibility (the snap sets `QT_QPA_PLATFORM=xcb`, so it also starts when the session asks for a Wayland Qt plugin).

### Is it available for Windows or macOS?

Not currently — the packaged builds are Linux only. The source is Python and PyQt5, so it may run elsewhere, but that is untested and unsupported.

### Can I contribute?

Yes. It is MIT licensed — open an [issue](https://github.com/rishabh3354/JPG2PDF/issues) or a pull request.

---

## ⚖️ How it compares

- **Online converters** (iLovePDF, Smallpdf, Zamzar) — convenient, but you upload your documents to someone else's server and hit size and daily limits. JPEG2PDF works offline with no limits.
- **`img2pdf` / ImageMagick** — excellent command-line tools, but no preview, no reordering and no encryption UI. JPEG2PDF is the graphical counterpart.
- **LibreOffice / GIMP export** — works in a pinch, but painful for batches of images.
- **Scanner suites** — heavier and usually tied to specific hardware.

---

## 🧩 More apps by Warlord Softwares

Other apps by Warlord Softwares are listed on [warlordsoftwares.com](https://warlordsoftwares.com/).

---

## 🔗 Links

- 📦 **Flathub:** [com.warlordsoftwares.jpeg2pdf](https://flathub.org/apps/details/com.warlordsoftwares.jpeg2pdf)
- 📦 **Snap Store:** [snapcraft.io/jpg2pdf](https://snapcraft.io/jpg2pdf)
- 🌐 **Website:** [warlordsoftwares.com](https://warlordsoftwares.com/)
- 🐞 **Issues:** [github.com/rishabh3354/JPG2PDF/issues](https://github.com/rishabh3354/JPG2PDF/issues)

---

## 📄 License

[MIT](LICENSE) © Rishabh Bhardwaj / Warlord Softwares.

Built with [PyQt5](https://pypi.org/project/PyQt5/), [Pillow](https://python-pillow.org/), [fpdf2](https://py-pdf.github.io/fpdf2/) and [pikepdf](https://pikepdf.readthedocs.io/).
