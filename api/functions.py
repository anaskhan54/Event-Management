from django.conf import settings
import urllib.request
import urllib.parse
import json
import os
from django.core.mail import EmailMessage
import qrcode
import base64
from cryptography.fernet import Fernet
from email.mime.image import MIMEImage
from PIL import Image
def verify_recaptcha(response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': response
            }
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    result = json.load(response)
    if result['success']:
        return True
    else:
        return False


def send_qr_code(email, student_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Assume `encrypt_data` is a placeholder for your encryption function
    encrypted_data = encrypt_data(student_id)
    qr.add_data(encrypted_data.decode())
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a file
    qr_img_path = os.path.join(settings.MEDIA_ROOT, f"qr_code_{student_id}.png")
    qr_img_pil = qr_img.convert('RGB')  # Convert PyPNGImage to PIL Image
    qr_img_pil.save(qr_img_path, format='PNG')
    # qr_img.save(qr_img_path, format="PNG")

    # Attach the QR code image to the email
    html_content = f"""
    <html>
    <body>
        <h2>Thank You for Registering, Here is Your QR</h2>
        <img src="cid:qr_code_{student_id}.png" alt="QR Code">
    </body>
    </html>
    """
    msg = EmailMessage(
        'QR Code for Student ID',
        html_content,
        settings.EMAIL_HOST_USER,
        [email],
    )
    msg.content_subtype = "html"

    with open(qr_img_path, "rb") as f:
        msg_img = MIMEImage(f.read())
        msg_img.add_header("Content-ID", f"<qr_code_{student_id}.png>")
        msg.attach(msg_img)

    msg.send()

    # Remove the temporary QR code image file
    os.remove(qr_img_path)
def encrypt_data(data):
    
    key=settings.AES_KEY.encode()
    cipher=Fernet(key)
    encrypted_data=cipher.encrypt(str(data).encode())
    return encrypted_data