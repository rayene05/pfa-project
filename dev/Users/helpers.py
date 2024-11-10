import secrets
from PIL import Image
import os
from dev import mail
from flask_mail import Message
from flask import url_for,current_app

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "ViRtualBanK Password Reset Request",
        sender="YOUR EMAIL",
        recipients=[user.email],
        body=f"""To reset your password, visit the following link:
        {url_for('users.reset_password', token=token, _external=True)}
        
        if you did not make this request, please ignore this email.""",
    )
    mail.send(msg)
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/user_pics", picture_name)
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name