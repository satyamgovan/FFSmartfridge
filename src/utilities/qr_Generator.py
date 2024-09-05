import qrcode


def generate_qr_code(item_name, item_description, expiry_date, volume):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr_data = f"Item Name: {item_name}\n" \
              f"Description: {item_description}\n" \
              f"Expiry Date: {expiry_date}\n" \
              f"Volume: {volume}"

    qr.add_data(qr_data)
    qr.make(fit=True)

    # Get the QR code as an image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a file
    img.save("../../img/qr/item_qr_code.png")

    print("Custom QR Code Data:")
    print(qr_data)


generate_qr_code("Tomato", "Fresh Tomato", "11/11/1111", 1.5)
