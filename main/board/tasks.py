from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Bullets
import datetime


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Bullets.objects.filter(dateCreation__gte=last_week)
    users = set(User.objects.values_list('users__email', flat=True))
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Новое за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
