from django.contrib.auth.models import User, Permission
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase
from okqa.qa.models import Question
import sending


class EmailTest(TestCase):

    def setUp(self):
        self.common_user = User.objects.create_user("commoner",
                                "commmon@example.com", "pass")
        self.candidate_user = User.objects.create_user("candidate",
                                "candidate@example.com", "pass")
        add_answer = Permission.objects.get(codename="add_answer")
        self.candidate_user.user_permissions.add(add_answer)
        self.q = Question.objects.create(author=self.common_user,
                        subject="why?")
        self.a = self.q.answers.create(author=self.candidate_user,
                        content="because\nthe world\nis round\n and a>b\n<b>bye bye</b>")
        self.site1 = Site.objects.create(domain='abc.com')
        self.site2 = Site.objects.create(domain='fun.com')
        self.q.tags.create(name="abc")
        self.q.tags.create(name="def")

    def test_new_answer_email(self):
        site = Site.objects.get_current()
        sending.send_new_answer(None, site, self.a)
        self.assertEqual(len(mail.outbox), 1)
#        print type(mail.outbox[0])
#        print mail.outbox[0].subject
#        print mail.outbox[0].body
#        print mail.outbox[0].alternatives[0][0]
#        assert False

    def tearDown(self):
        self.q.delete()
        User.objects.all().delete()
