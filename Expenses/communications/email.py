from django.core.mail import send_mail
from django.conf import settings

import logging

from ..models import User
from .base import addToArchives


logger = logging.getLogger('Expenses')


def sendNotificationEmail(notification):
    try:
        # Send the email
        users = User.objects.all()
        emailFrom = settings.EMAIL_HOST_USER
        subject = f"Notification: {notification.category}"
        payAt = f"Pay at: {notification.bill}" if notification.bill else ""
        message = f"{notification.message}\n{notification.amount}{notification.currency}\n{payAt}"

        recipientList = []
        for user in users:
            recipientList.append(user.email)

        send_mail(subject, message, emailFrom, recipientList)
        addToArchives(subject, message, recipientList)

    except Exception as e: 
        logger.error(f'Error in sending automated email: {e}')


def sendReminderEmail(finalUserBalance, currentUser):
    try:
        # Send email to users who owe the current user
        emailFrom = settings.EMAIL_HOST_USER
        for user, balance_info in finalUserBalance.items():
            balance = balance_info['balance']
            # Only email users who owe money to the current user
            if balance > 0:
                subject = 'You Owe a Balance'
                message = f"Hi {user.first_name},\n\nYou owe {currentUser.first_name} an amount of {abs(balance):.2f} €.\n\nPlease settle your balance at your earliest convenience."
                recipientList = [user.email]  # Email to the user who owes money
                send_mail(subject, message, emailFrom, recipientList)
                addToArchives(subject, message, recipientList)

    except Exception as e: 
        logger.error(f'Error in sending reminder email: {e}')