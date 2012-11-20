import json
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.template.context import RequestContext
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site, get_current_site
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from taggit.utils import parse_tags

from okqa.qa.forms import AnswerForm, QuestionForm
from .models import *
import signals

from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from okqa.qa.mixins import JSONResponseMixin
from django.forms.models import model_to_dict


# the order options for the list views
ORDER_OPTIONS = {'date': '-created_at', 'rating': '-rating'}


def home(request):
    return render(request, "home.html")

def questions(request, tags=None):
    """
    list questions ordered by number of upvotes
    """

    context = {}
    order_opt = request.GET.get('order', 'rating')
    order = ORDER_OPTIONS[order_opt]

    if tags:
        tags_list = tags.split(',')
        questions = Question.on_site.filter(tags__name__in=tags_list)
        context['current_tags'] = tags_list
    else:
        questions = Question.on_site.order_by(order)
        context['tags'] = TaggedQuestion.on_site.values('tag__name').annotate(count=Count("tag"))

    context['questions'] = questions
    context['by_date'] = order_opt == 'date'
    context['by_rating'] = order_opt == 'rating'
    return render(request, "qa/question_list.html", context)

def tagged_questions(request, tags):

    return questions(request, tags_list)

    questions.order_by(ORDER_OPTIONS[request.GET.get('order', 'date')])

    return render(request, "qa/question_list.html", dict(questions=questions,
                                        current_tags=tags_list))

def view_question(request, q_id):
    question = get_object_or_404(Question, id=q_id)
    can_answer = question.can_answer(request.user)
    context = RequestContext(request, {"question": question,
        "answers": question.answers.all(),
        })
    if can_answer:
        try:
            user_answer = question.answers.get(author=request.user)
            context["my_answer_form"] = AnswerForm(instance=user_answer)
            context["my_answer_id"] = user_answer.id
        except question.answers.model.DoesNotExist:
            context["my_answer_form"] = AnswerForm()
            context["can_answer"] = True

    if request.user.is_authenticated() and \
       not request.user.upvotes.filter(question=question).exists():
        context["can_upvote"] = True
    else:
        context["can_upvote"] = False

    return render(request, "qa/question_detail.html", context)


class QuestionDetail(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Question
    template_name = 'qa/question_detail.html'
    context_object_name = 'question'
    slug_field = 'unislug'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        can_answer = self.object.can_answer(self.request.user)

        context['answers'] = self.object.answers.all()
        if can_answer:
            try:
                user_answer = self.object.answers.get(author=self.request.user)
                context['my_answer_form'] = AnswerForm(instance=user_answer)
                context['my_answer_id'] = user_answer.id
            except self.object.answers.model.DoesNotExist:
                context['my_answer_form'] = AnswerForm()
                context['can_answer'] = True

        if self.request.user.is_authenticated() and \
           not self.request.user.upvotes.filter(question=self.object).exists():
            context['can_upvote'] = True
        else:
            context['can_upvote'] = False

        return context

    def render_to_response(self, context):
            # Look for a 'format=json' GET argument
            if self.request.GET.get('format', 'html') == 'json' or self.request.is_ajax():
                data = {
                    'question': {
                        'subject': self.object.subject,
                        'content': self.object.content,
                        'author': self.object.author.username
                    }
                }

                return JSONResponseMixin.render_to_response(self, data)
            else:
                return SingleObjectTemplateResponseMixin.render_to_response(self, context)


@login_required
def post_answer(request, q_id):

    is_new = True

    question = Question.objects.get(id=q_id)

    if not question.can_answer(request.user):
        return HttpResponseForbidden(_("You must be logged in as a candidate to post answers"))

    try:
        # make sure the user haven't answered already
        answer = question.answers.get(author=request.user)
        is_new = False

    except question.answers.model.DoesNotExist:
        answer = Answer(author=request.user, question=question)

    answer.content = request.POST.get("content")

    answer.save()

    if is_new:
        signals.answer_posted.send(sender=None, site=get_current_site(request), answer=answer)

    return HttpResponseRedirect(question.get_absolute_url())


@login_required
def post_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            signals.question_posted.send(sender=None, site=get_current_site(request), question=question)
            return HttpResponseRedirect(question.get_absolute_url())

        #TODO: make this better - show the form
        # return HttpResponseRedirect("/#question_modal")
    elif request.method == "GET":
        form = QuestionForm()

    return render(request, "qa/post_question.html", {"form": form})


@login_required
def upvote_question(request, q_id):
    if request.method == "POST":
        q = get_object_or_404(Question, id=q_id)
        user = request.user

        if q.author == user or user.upvotes.filter(question=q):
            return HttpResponseForbidden(_("You already upvoted this question"))
        else:
            upvote = QuestionUpvote.objects.create(question=q, user=user)
            #TODO: use signals so the next line won't be necesary
            new_count = increase_rating(q)
            return HttpResponse(new_count)
    else:
        return HttpResponseForbidden(_("Use POST to upvote a question"))


@transaction.commit_on_success
def increase_rating(q):
    q = Question.objects.get(id=q.id)
    q.rating += 1
    q.save()
    return q.rating


class RssQuestionFeed(Feed):
    """Simple feed to get all questions"""
    title = _('OK QA Question Feed')
    link = "/"
    description = _('Questions from OKQA')

    def items(self):
        return Question.objects.order_by('-updated_at')

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return item.content


class AtomQuestionFeed(RssQuestionFeed):
    feed_type = Atom1Feed
    subtitle = RssQuestionFeed.description


class RssQuestionAnswerFeed(Feed):
    """"Give question, get all answers for that question"""

    def get_object(self, request, q_id):
        return get_object_or_404(Question, pk=q_id)

    def title(self, obj):
        return _('Answers for the question') + ' "%s' % obj.subject + '"'

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _('A feed of all answers for the question') + ' "%s' % obj.subject + '"'

    def items(self, obj):
        return Answer.objects.filter(question=obj).order_by('-updated_at')


class AtomQuestionAnswerFeed(RssQuestionAnswerFeed):
    feed_type = Atom1Feed
    subtitle = RssQuestionAnswerFeed.description

@login_required
@require_POST
def flag_question(request, q_id):
    q = get_object_or_404(Question, id=q_id)
    user = request.user

    if user.flags.filter(question=q):
        return HttpResponseForbidden(_("You already reported this question"))
    else:
        flag = QuestionFlag.objects.create(question=q, reporter=user)
        #TODO: use signals so the next line won't be necesary
        new_count = q.flagged()
        return HttpResponse(new_count)
