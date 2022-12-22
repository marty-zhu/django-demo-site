from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect # Http404
from django.urls import reverse
from django.db.models import Count

# for Django "generic view" refactoring
from django.views import generic
# from django.template import loader

from .models import Question, Choice

# Switched to Django "generic view" system
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     # with the `render` shortcut:
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")

#     # with `get_object_or_404` shortcut
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# Django "generic views" system START

class IndexView(generic.ListView):  # to show a list of items
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).annotate(
            num_choices=Count('choice')
        ).filter(
            num_choices__gt=0
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):  # to show details on one list item
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Exclude any questions that are not published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Exclude any question that are not published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

# Django "generic views" system END

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
