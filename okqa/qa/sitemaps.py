from django.contrib.sitemaps import GenericSitemap
from django.contrib.auth.models import User
from okqa.qa.models import Question
from okqa.user.candidates import candidate_group

question_dict = {
    'queryset': Question.objects.all(),
    'date_field': 'updated_at',
}

candidate_dict = {
    'queryset': User.objects.filter(groups__in=[candidate_group]),
    'date_field': 'last_login',
}

sitemaps = {
    'questions': GenericSitemap(question_dict, priority=1, changefreq='hourly'),
    'candidates': GenericSitemap(candidate_dict, priority=0.6, changefreq='weekly'),
}
