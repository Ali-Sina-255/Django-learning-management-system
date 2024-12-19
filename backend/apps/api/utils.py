import datetime

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(request, user):
    """Send the activation email with the verification link."""
    # Get the current site domain for the URL
    current_site = get_current_site(request)
    protocol = (
        "https" if request.is_secure() else "http"
    )  # Handle secure protocol (HTTP/HTTPS)

    # Generate the token and uid
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # Create the activation link
    activation_link = (
        f"{protocol}://{current_site.domain}/users/activate/{uid}/{token}/"
    )

    print(f"Generated Activation Link: {activation_link}")

    # Get the current year for the footer
    current_year = datetime.datetime.now().year

    # Prepare the email message
    email_subject = "Activate Your Account"
    email_message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": uid,
            "token": token,
            "activation_link": activation_link,  # Pass the full URL here
            "current_year": current_year,  # Pass current year for footer
        },
    )

    email = EmailMessage(
        subject=email_subject,
        body=email_message,
        to=[user.email],
    )
    email.content_subtype = "html"  
    email.send()


def send_reset_password_email(request, user):
    form_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    email_subject = "Reset your password "
    message = render_to_string(
        "accounts/email/reset_password_email.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(email_subject, message, form_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()


