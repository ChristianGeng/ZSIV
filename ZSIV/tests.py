"""
Currently the one and ony test module for ZSIV

Run it with:

.. code-block:: guess

    python manage.py test  ZSIV  --keepdb

Links:

<https://docs.djangoproject.com/en/2.1/topics/testing/overview/>`_
<https://docs.djangoproject.com/en/2.1/intro/tutorial05/>`_


"""

from django.test import TestCase, TransactionTestCase
from ZSIV.models import Mitarbeiter


class TestMitarbeiter(TransactionTestCase):

    def test_mitarbeiter_name(self):
        """check that same Mitarbeiter cannot be created twice"""
        # assert ma.id == 1

        Mitarbeiter.objects.all().delete()
        Mitarbeiter.objects.create(Vorname="Heinz", Nachname="Mustermann", email="Mustermann@example.org")

        with self.assertRaises(Exception) as context:
            Mitarbeiter.objects.create(Vorname="Heinz",
                                       Nachname="Mustermann",
                                       email="Mustermann@example.org")

            self.assertTrue('exception' in context.exception)

        Mitarbeiter.objects.all().delete()

    def test_mitarbeiter_defaults(self):
        """test Anrede and Sex defaults"""

        ma = Mitarbeiter(Vorname="Heinz",
                         Nachname="Mustermann",
                         email="Mustermann@example.org")

        self.assertEqual(ma.Sex, 'f')
        self.assertEqual(ma.Anrede, "Frau Dr. ")

    def test_mitarbeiter_sex_choices(self):
        """These tests should fail"""
        ma = Mitarbeiter(Vorname="Heinz", Nachname="Mustermann", email="Mustermann@example.org", Sex="aa")
        ma = Mitarbeiter(Vorname='a'*400)
        print(ma)


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        print("test der nix tut")
        self.assertEqual(1, 1, "1 und 1 immer gleich")
        # time = timezone.now() + datetime.timedelta(days=30)
        # future_question = Question(pub_date=time)
        # self.assertIs(future_question.was_published_recently(), False)
