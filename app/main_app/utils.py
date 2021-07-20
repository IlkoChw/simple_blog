from django.core.mail import send_mail
from django.conf import settings
import logging


logger = logging.getLogger(__name__)


def get_target_subscribers(author_pk):
    from .models import UserProfile
    author = UserProfile.objects.get(pk=author_pk)
    target_subscribers = author.user.subscriptions.all()

    for subscriber in target_subscribers:
        yield subscriber


def sent_email_wrapper(subject, message, subscriber_email):
    try:
        logger.info(f'Отправка сообщения на почту {subscriber_email}')
        send_mail(subject, message, settings.EMAIL_HOST_USER, [subscriber_email],)
    except Exception as e:
        logger.error(f'Ошибка отправки на почту {subscriber_email}\n({e})')


def new_post_email_sent(post_pk):
    from .models import Post

    post = Post.objects.get(pk=post_pk)

    subject = f'Новый пост: {post.title}. от {post.author}'
    message = f'http://127.0.0.1:8000/feed/'

    subscribers = get_target_subscribers(post.author.pk)

    for subscriber in subscribers:
        sent_email_wrapper(subject, message, subscriber)



