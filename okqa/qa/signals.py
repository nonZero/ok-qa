import django.dispatch

answer_posted = django.dispatch.Signal(providing_args=["site", "answer"])
question_posted = django.dispatch.Signal(providing_args=["site", "question"])
