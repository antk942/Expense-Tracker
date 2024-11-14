from django.utils import timezone
from django.conf import settings

from .models import Notification
from .communications import email

import logging
import os
import shutil
import datetime


logger = logging.getLogger('Expenses')


def checkAndSendNotifications():
    logger.info('checkAndSendNotifications started with interval 1 hour..')
    try:
        # Get the current date
        today = timezone.now().date()

        # Query notifications that are due to be sent today
        notificationsToSend = Notification.objects.filter(dueDate=today)

        for notification in notificationsToSend:
            email.sendNotificationEmail(notification)
            # After sending the email, recalculate the next frequencyDate and save it
            notification.dueDate = notification.calculateNextDate()
            notification.save()

            # Delete notification if it was a one time thing
            if notification.frequency == 'Once':
                notification.delete()    

    except Exception as e:
        logger.error(f'Error in checkAndSendNotifications: {e}')

    logger.info('Task checkAndSendNotifications finished!')


def backupDatabase():
    # Backs up the SQLite database to a folder named with the current date.
    
    try:
        logger.info('backupDatabase started with interval 1 week..')        
        
        # Get today's date in DDMMYYYY format
        today = datetime.datetime.now().strftime("%d%m%Y")
        
        # Create the backup directory for today's date
        backup_path = os.path.join(settings.BACKUP_DIR, today)
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy the SQLite database to the backup folder
        shutil.copy2(settings.DB_PATH, os.path.join(backup_path, 'db.sqlite3'))
        
        logger.info(f"Backup created at: {os.path.join(backup_path, 'db.sqlite3')}")

    except Exception as e:
        logger.error(f'Error in backupDatabase: {e}')

    logger.info('Task backupDatabase finished!')