from django.core.mail import send_mail

def send_employee_email(employee,system_generated_password,business):
    subject = "Welcome to [Your Company Name]!"
    message = f"""
    Dear {employee.first_name} {employee.last_name},

    Welcome to {business}! 🎉 We're excited to have you on board.

    Here are your login details:
    🔑 **Username:** {employee.email}
    🔒 **Temporary Password:** {system_generated_password}

    For security reasons, please **change your password** after your first login.

    If you have any questions, feel free to contact our support team at [Support Email].

    Best regards,  
    [Your Company Name]  
    [Company Website]
    """

    # Send the email
    send_mail(
        subject,
        message,
        "eduarc4life@gmail.com",  # Sender email
        [employee.email],  # Recipient email
        fail_silently=False,
    )
