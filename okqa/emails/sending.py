from okqa.emails.routing import get_recipients_for_new_question, \
    get_recipients_for_new_answer
from templated_email import send_templated_mail
import logging


def send_new_answer(sender, site, answer, **kwargs):

    for user in get_recipients_for_new_answer(answer):
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
                # headers={'My-Custom-Header':'Custom Value'},
        )


def send_new_question(sender, site, question, **kwargs):

    for user in get_recipients_for_new_question(question):
        logging.info('Sending new question notification to %s' % user.email)

        send_templated_mail(
                template_name='new_question',
                from_email=None,
                recipient_list=[user.email],
                context={
                    'site': site,
                    'question': question,
                    'user': user,
                },
                # headers={'My-Custom-Header':'Custom Value'},
        )
