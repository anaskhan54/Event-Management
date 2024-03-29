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
from datetime import datetime, timedelta
import jwt
import secrets
import string

access_secret=settings.ACCESS_SECRET_KEY
refresh_secret=settings.REFRESH_SECRET_KEY


def generate_verification_token():
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(20))
    return token


def time_left(target_date):
    target_date = datetime.strptime(target_date, "%d/%m/%Y %H:%M")
    current_date = datetime.now()
    
    time_difference = target_date - current_date
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return days, hours, minutes, seconds

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


def send_qr_code(email, student_id,student_name):
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
    current_dir = os.path.dirname(os.path.abspath(__file__))

    insta_img_path = os.path.join(current_dir, "insta.png")
    linkedin_img_path = os.path.join(current_dir, "linkedin.png")
    logo_img_path = os.path.join(current_dir, "logo.png")
    qr_img_pil = qr_img.convert('RGB')  # Convert PyPNGImage to PIL Image
    qr_img_pil.save(qr_img_path, format='PNG')
    # qr_img.save(qr_img_path, format="PNG")

    # Attach the QR code image to the email
    html_content = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                max-width: 150px;
            }}
            .qr-code {{
                max-width: 200px;
                margin: 20px auto;
                display: block;
            }}
            .social-logos {{
                text-align: center;
            }}
            .social-logo {{
                max-width: 30px;
                margin: 0 5px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="cid:logo.png" alt="Programming Club Logo" class="logo">
            <h2>Thank You for Registering!</h2>
            <p>Dear {student_name},</p>
            <p>We are excited to have you join our event. Here is your registration confirmation:</p>
            <img src="cid:qr_code_{student_id}.png" alt="QR Code" class="qr-code">
            <p>Now, to complete your registration, please go to the registration desk and pay Rs.150. Show this QR code at the desk, and the same QR code will serve as your ticket after the payment.</p>
            <p>For any queries, please contact our coordinator:</p>
            <p>Name: Coordinator Name</p>
            <p>Mobile Number: Coordinator Mobile Number</p>
            <p>Best regards,</p>
            <p>Your Programming Club</p>
            <hr>
            <div class="social-logos">
                <a href="https://www.instagram.com/" target="_blank"><img src="cid:insta.png" alt="Instagram Logo" class="social-logo" style="height: 30px; width: 30px;"></a>
                <a href="https://www.linkedin.com/" target="_blank"><img src="cid:linkedin.png" alt="LinkedIn Logo" class="social-logo" style="height: 30px; width: 30px;"></a>
            </div>
        </div>
    </body>
    </html>
    """
    msg = EmailMessage(
        'QR Code for Payment and Ticket',
        html_content,
        settings.EMAIL_HOST_USER,
        [email],
    )
    msg.content_subtype = "html"

    # Attach the logo
    with open(logo_img_path, 'rb') as f:
        logo_data = f.read()
        msg_img = MIMEImage(logo_data)
        msg_img.add_header('Content-ID', '<logo.png>')
        msg.attach(msg_img)

    # Attach the QR code
    with open(qr_img_path, 'rb') as f:
        qr_code_data = f.read()
        msg_qr_code = MIMEImage(qr_code_data)
        msg_qr_code.add_header('Content-ID', f'<qr_code_{student_id}.png>')
        msg.attach(msg_qr_code)

    # Attach the Instagram logo
    with open(insta_img_path, 'rb') as f:
        insta_data = f.read()
        msg_insta = MIMEImage(insta_data)
        msg_insta.add_header('Content-ID', '<insta.png>')
        msg.attach(msg_insta)

    # Attach the LinkedIn logo
    with open(linkedin_img_path, 'rb') as f:
        linkedin_data = f.read()
        msg_linkedin = MIMEImage(linkedin_data)
        msg_linkedin.add_header('Content-ID', '<linkedin.png>')
        msg.attach(msg_linkedin)

    msg.send()

    # Remove the temporary QR code image file
    os.remove(qr_img_path)
def encrypt_data(data):
    
    key=settings.AES_KEY.encode()
    cipher=Fernet(key)
    encrypted_data=cipher.encrypt(str(data).encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    key = settings.AES_KEY.encode()
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

def generate_tokens(id):
    access_token_payload={
        'id':id,
        'exp':int((datetime.now()+timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRY))).timestamp())
    }
    refresh_token_payload={
        'id':id,
        'exp':int((datetime.now()+timedelta(days=int(settings.REFRESH_TOKEN_EXPIRY))).timestamp())
    }
    access_token=jwt.encode(access_token_payload, access_secret, algorithm='HS256')
    refresh_token=jwt.encode(refresh_token_payload, refresh_secret, algorithm='HS256')
    return access_token.encode().decode(), refresh_token.encode().decode()

def is_refresh_valid(refresh_token):
    try:
        payload=jwt.decode(refresh_token, refresh_secret, algorithms=['HS256'])
        
        exp=payload['exp']
        
        current_time=int(datetime.now().timestamp())
        if current_time>exp:
            return False
        else:  
            return True
    except:
        return False
def is_access_valid(access_token):
    try:
        payload=jwt.decode(access_token, access_secret, algorithms=['HS256'])
        
        exp=payload['exp']
        
        current_time=int(datetime.now().timestamp())
        if current_time>exp:
            return False
        else:  
            return True
    except:
        return False
    
def send_verification_email(college_email,token):
    html_content=f"""
    <html>
    <body>
        <h2>Thank You for Registering, Please Verify Your Email</h2>
        <a href="https://pc.anaskhan.site/api/verify_email?token={token}">Click here to verify your Email</a>
    </body>
    </html>
    """
    msg=EmailMessage(
        'Verify Your Email',
        html_content,
        settings.EMAIL_HOST_USER,
        [college_email],
    )
    msg.content_subtype="html"
    msg.send()