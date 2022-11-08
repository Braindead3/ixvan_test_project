import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Transaction

today = datetime.date.today()


def send_email(user_email: str, subject: str, message: str) -> None:
    """
    Отправляет сообщение на емаил
    :param user_email: емеил пользователя
    :param subject: заголовок письма
    :param message: содержание писамьа
    :return: None
    """
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user_email])


def create_statistics(user: User) -> dict:
    """
    Собирается статистика о том сколько пользовотель потратил вчера и за в целом за месяц.

    :param user: Пользователь
    :return: Возвращает словарь со статистикой
    """
    stat = {'day_spending': 0,
            'total_spending': 0}
    previous_day_transactions = Transaction.objects.filter(user=user,
                                                           time__year=today.year,
                                                           time__month=today.month,
                                                           time__day=today.day - 1,
                                                           type='debit')
    for transaction in previous_day_transactions:
        stat['day_spending'] = stat['day_spending'] + transaction.sum

    month_transactions = Transaction.objects.filter(user=user,
                                                    time__year=today.year,
                                                    time__month=today.month,
                                                    type='debit')

    for transaction in month_transactions:
        stat['total_spending'] = stat['day_spending'] + transaction.sum

    print(stat)
    return stat
