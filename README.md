# Python Projects

This repository contains two simple Python command-line tools:

## 1. `qr_generator.py`
Generates a QR code from:
- A URL or text you type manually
- A text file

🖼 Saves the QR code as an image and opens it.  
🅰 Optionally displays it as ASCII in the terminal.

---

## 2. `notes_app.py`
A secure notes app for the terminal:
- Add, view, delete, and export notes
- All note content is encrypted using **Fernet symmetric encryption**
- Notes are stored in a `data.json` file

---

### 🔧 Requirements

Install dependencies:

```bash
pip install qrcode pyqrcode pypng cryptography
