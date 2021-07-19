import os
from random import randrange, seed
from datetime import datetime

from django.core.mail import send_mail as sm
from django.conf import settings



def get_random_text(text_length: int) -> str:
    """
    generates random text of required length
    """
    try:
        raw_text: str = "6k-d4qe2ebrwpp3r+_@s%c!77gp#r(b&ia_jzt0l%+h=nebwt"
        seed = datetime.now()
        random_text: str = ""
        counter: int = 1
        text_length = int(text_length)
        while counter <= text_length:
            random_text += raw_text[randrange(0, len(raw_text))]
            counter += 1
    except ValueError as err:
        print("An integer is required")
    return random_text

def send_mail(subject: str, message: str, recipient_list: list = None) -> list:
    return sm(
        subject = subject,
        message = message,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = recipient_list,
        fail_silently=False,
    ) 
