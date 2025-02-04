import os
import secrets

from PIL import Image
from flask import current_app, url_for
from flask_mail import Message

from webapp import mail
from webapp.users.models import User


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_fn)
    
    output_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreply@demo.com', 
                  recipients=[user.email])
    
    msg.body = f""" To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, then simply ignore this email and no changes will be made.
"""
    mail.send(msg)
