import os
import sys

import django


def initial():
    sys.path.append('../..')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reservation.settings'
    django.setup()


initial()

from management.models import User

User.objects.bulk_create(
    [
        User(username='owner1'),
        User(username='owner2'),
        User(username='owner3'),
        User(username='user1'),
        User(username='user2'),
        User(username='user3'),
    ]
)
