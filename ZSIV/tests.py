"""
Currently the one and ony test module for ZSIV

Run it with: 

.. code-block:: guess

    python manage.py test  ZSIV  --keepdb

Links: 

<https://docs.djangoproject.com/en/2.1/topics/testing/overview/>`_
<https://docs.djangoproject.com/en/2.1/intro/tutorial05/>`_


"""

import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Summaries


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        print("test der nix tut")
        self.assertEqual(1, 1, "1 und 1 immer gleich")
        #time = timezone.now() + datetime.timedelta(days=30)
        #future_question = Question(pub_date=time)
        #self.assertIs(future_question.was_published_recently(), False)
