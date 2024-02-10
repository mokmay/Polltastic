from django.test import TestCase
from polls.models import Question
from django.utils import timezone
import datetime


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

