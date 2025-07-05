import qrcode
import os

def generate_qr():
    try:
        # Asking for file input
        file_path = input("optional,Enter path to a text file to encode (or press Enter to type text/URL): ").strip()
        if file_path:
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = f.read()
            else:
                print("File not found.")
                return
        else:
            data = input("Enter the text or URL to encode in the QR code: ")
            if not data.strip():
                print("Input cannot be empty.")
                return

        filename = input("Enter filename to save (optional, default: my_qrcode.png): ").strip()
        if not filename:
            filename = "my_qrcode.png"
        elif not filename.lower().endswith('.png'):
            filename += ".png"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(f"QR code successfully saved as '{filename}'")

        # Display ASCII QR code
        try:
            import pyqrcode
            qr_ascii = pyqrcode.create(data)
            print(qr_ascii.terminal(quiet_zone=1))
        except ImportError:
            print("Install 'pyqrcode' to see ASCII QR code in the console: pip install pyqrcode pypng")

        # Open the image (cross-platform)
        import webbrowser
        webbrowser.open('file://' + os.path.realpath(filename))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_qr()