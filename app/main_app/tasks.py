from background_task import background
from .utils import new_post_email_sent


@background()
def task_new_post_email(post_pk):
    new_post_email_sent(post_pk)
