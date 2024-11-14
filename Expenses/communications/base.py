from django.conf import settings

import os
from datetime import datetime


def addToArchives(subject, message, recipientList, direc=settings.ARCHIVES_DIR):
    date_str = datetime.now().strftime("%d-%m-%Y")
    file_name = ''
    archive_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), direc)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    
    file_path = os.path.join(archive_dir, f"{file_name}{date_str}.txt")

    with open(file_path, 'a') as file:
        file.write(f"To: {recipientList}\n")
        file.write(f"Subject: {subject}\n")
        file.write(f"Message: {message}\n")
        file.write("\n")