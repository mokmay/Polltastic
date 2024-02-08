import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed.
        """
        #Arrange
        #Act
        response = self.client.get(reverse("polls:index"))
        #Assert
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        questions with a pub_date in the past are displayed on the index page.
        """
        #Arrange
        question = create_question(question_text="Past question.", days=-30)
        #Act
        response = self.client.get(reverse("polls:index"))
        #Assert
        self.assertQuerySetEqual(
                response.context["latest_question_list"],
                [question],
                )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        #Arrange
        create_question(question_text="Future question.", days=30)
        #Act
        response = self.client.get(reverse("polls:index"))
        #Assert
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        #Arrange
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        #Act
        response = self.client.get(reverse("polls:index"))
        #Assert
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        #Arrange
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        #Act
        response = self.client.get(reverse("polls:index"))
        #Assert
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        #AAA - Arrange Act Assert
        #Arrange
        time = timezone.now() + datetime.timedelta(days =30)
        future_question = Question(pub_date=time)
        #Act
        result = future_question.was_published_recently()
        #Assert
        self.assertIs(result, False)

    def test_was_published_recently_with_no_recent_questions(self):
        #Arrange
        time = timezone.now() - datetime.timedelta(days=30)
        no_recent_question = Question(pub_date=time)
        #Act
        result = no_recent_question.was_published_recently()
        #Assert
        self.assertIs(result, False)

    def test_was_published_recently_with_recent_questions(self):
        time = timezone.now() - datetime.timedelta(hours=12)
        recent_question = Question(pub_date=time)
        #Act
        result = recent_question.was_published_recently()
        #Assert
        self.assertIs(result, True)
