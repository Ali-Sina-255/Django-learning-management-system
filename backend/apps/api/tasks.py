# tasks.py
from config.celery import app
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@app.task
def send_reset_password_email(user_id, link):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    form_email = settings.DEFAULT_FROM_EMAIL
    email_subject = "Reset your password"

    # Fetch the domain from the Site model
    current_site = Site.objects.get_current()
    domain = current_site.domain

    message = render_to_string(
        "account/email/reset_password_email.html",
        {
            "user": user,
            "domain": domain,  # Use domain directly
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
            "link": link,
        },
    )
    to_email = user.email
    mail = EmailMessage(email_subject, message, form_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()
