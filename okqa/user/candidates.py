from django.conf import settings
from django.contrib.auth.models import Group

candidate_group = Group.objects.get_or_create(name=settings.CANDIDATES_GROUP_NAME)[0]
