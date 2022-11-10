from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib.auth.models import User

from .utils import send_email, create_statistics


@shared_task()
def send_email_with_statistics():
    print('task')
    users: list[User] = User.objects.all()
    for user in users:
        if user.username != 'admin':
            if user.email is not None:
                stat = create_statistics(user)
                user_email = user.email
                subject = f'Статистика на сегодня'
                email_body = f'Было потрачено вчера ${stat.get("day_spending")}.' \
                             f' Было потрачено за месяц {stat.get("total_spending")} \n '

                send_email(user_email, subject, email_body)
