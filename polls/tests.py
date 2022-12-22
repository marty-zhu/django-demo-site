import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.
class QuestionModelPublishedRecentlyTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns `False` for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns `False` for questions whose pub_date is older than 1 day.
        """
        one_day_ago = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=one_day_ago)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns `True` for questions whose pub_date is within the last day.
        """
        same_day = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=same_day)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days, without_choices=False):
    """
    Create a question with the given `question_text` and published the given number of `days` offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question.objects.create(question_text=question_text, pub_date=time)
    if !without_choices:
        q.choice_set.create(choice_text="Choice 1", votes=0)
    return q

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        question = create_question("Past question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page.
        """
        create_question("Future question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.
        """
        question = create_question("Past question.", -30)
        create_question("Future question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question("Past question 1.", -30)
        question2 = create_question("Past question 2.", -15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )

class QuestionDetailsViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a publication date in the future returns a 404 not found error.
        """
        future_question = create_question("Future question.", 30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a publication date in the past displays the question's text.
        """
        past_question = create_question("Past question.", -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):

    def test_future_question(self):
        """
        The results view of a question with a publication date in the future returns a 404 not found error.
        """
        future_question = create_question("Future question.", 30)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The results view of a question with a publication date in the pastdisplays thest question's text.
        """
        past_question = create_question("Past question.", -30)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionsWithoutChoicesIndexViewTest(TestCase):

    def test_question_with_choices(self):
        """Past question with choices are shown in the index view."""
        question_with_choice = create_question("Question with choice", -30)
        question_with_choice.choice_set.create(choice_text="Choice 1", votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question_with_choice])

    def test_question_without_choices(self):
        """Past question with no choices are not shown in the index view."""
        question_without_choices = create_question("Question without choices", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
