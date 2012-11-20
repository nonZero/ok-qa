from templated_email import send_templated_mail
import logging
from django.conf import settings


def send_new_answer(sender, site, answer, **kwargs):

    recipients = [answer.question.author]

    for user in recipients:
        logging.info('Sending new answer notification to %s' % user.email)

        send_templated_mail(
                template_name='new_answer',
                from_email=None,
                recipient_list=[user.email],
                context={
                    'site': site,
                    'answer': answer,
                    'user': user,
                },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                # headers={'My-Custom-Header':'Custom Value'},
                # template_prefix="my_emails/",
                # template_suffix="email",
        )
