import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_forgot_password_email_custom_admin(context, recipient_list):
    """
    Sends a forgot password email with a reset link to the user.

    :param context: Dictionary containing the data to render the email template.
                    Example: {"username": "JohnDoe", "reset_password_url": "https://example.com/reset"}
    :param recipient_list: List of email addresses to send the email to.
    """
    subject = "Password Reset Request"
    # html_message = render_to_string("admin/forgot_password.html", context)
    # plain_message = strip_tags(html_message)  # Fallback for email clients that do not support HTML
    from_email = "noreply@example.com"  # Default sender email

    send_mail(
        subject=subject,
        message="Your forget password send email function is executed",
        from_email=from_email,
        recipient_list=recipient_list,
        # html_message=html_message,
    )
