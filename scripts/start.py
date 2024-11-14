import os


commands = [
    'python manage.py collectstatic',
    'python manage.py migrate',
]

for command in commands:
    os.system(command)