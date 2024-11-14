import os


commands = [
    'python manage.py crontab remove',
    'python manage.py crontab add',
    'python manage.py crontab show'
]

for command in commands:
    os.system(command)