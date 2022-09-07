from django.test import TestCase
from django.utils import timezone
import datetime
from django.urls import reverse
from .models import Question

class QuestionModelTest(TestCase):
  def test_was_published_future(self):
    """ test number one"""
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(question_text="¿Cuantos arboles hay en todo el planeta?",pub_date=time)
    self.assertIs(future_question.was_published_recently(), False)
  
  def test_published_recently(self):
    """ test number two"""
    time = timezone.now() + datetime.timedelta(days=0)
    recent_question = Question(question_text="¿Que hojas de colores son las mas vendidas?",pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)

  def test_was_published_before(self):
    """ test number three"""
    time = timezone.now() + datetime.timedelta(days=-15)
    before_question = Question(question_text="¿Cual es el mejor lenguaje de programacion?",pub_date=time)
    self.assertIs(before_question.was_published_recently(), False)


def create_question(question_text,days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTest(TestCase):
  def test_no_questions(self):
    """ test number one views """
    response = self.client.get(reverse("polls:index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context["latest_question_list"], [])

  def test_future_question(self):
    create_question("Future question", days=30)
    response = self.client.get(reverse("polls:index"))
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context["latest_question_list"], [])

  def test_past_question(self):
    question = create_question("Past question", days=-10)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerysetEqual(response.context["latest_question_list"], [question])

  def test_future_question_and_past_question(self):
    past_question = create_question("Past question", days=-30)
    future_question = create_question("Future question", days=30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerysetEqual(
      response.context["latest_question_list"], [past_question]
    )


  def test_two_question(self):
    past_question = create_question("Past question number one", days=-30)
    past_question_two = create_question("Past question number two", days=-40)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerysetEqual(
      response.context["latest_question_list"], [past_question_two,past_question]
    )


class QuestionDetailViewTest(TestCase):
  def test_future_question(self):
    future_question = create_question("Future question", days=30)
    url = reverse("polls:detail",args=(future_question.pk,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)

  def test_past_question(self):
    past_question = create_question("Past question", days=-30)
    url = reverse("polls:detail",args=(past_question.pk,))
    response = self.client.get(url)
    self.assertContains(response, past_question.question_text)