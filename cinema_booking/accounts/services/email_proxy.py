from abc import ABC, abstractmethod
from django.core.mail import send_mail
from django.conf import settings


class EmailServiceInterface(ABC):
    @abstractmethod
    def send_email(self, subject, message, recipient_list, from_email=None):
        pass


class DjangoEmailService(EmailServiceInterface):
    def send_email(self, subject, message, recipient_list, from_email=None):
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        return send_mail(subject, message, from_email, recipient_list)


class EmailProxy(EmailServiceInterface):
    def __init__(self, email_service):
        self.email_service = email_service

    def send_email(self, subject, message, recipient_list, from_email=None):
        # Log the email details
        print(f"Sending email to: {recipient_list} | Subject: {subject}")
        
        try:
            # Delegate to the actual email service
            return self.email_service.send_email(subject, message, recipient_list, from_email)
        except Exception as e:
            # Handle or log exceptions
            print(f"Failed to send email: {e}")
            raise
