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

import unittest
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

class TestSendgrid(unittest.TestCase):

    def test_sendgrid_send_message(self):
        send_mail("Your Subject", "This is a simple text email body.",
                  "Yamil Asusta <hello@yamilasusta.com>", ["yamil@sendgrid.com"])

        mail = EmailMultiAlternatives(
            subject="Your Subject",
            body="This is a simple text email body.",
            from_email="Christian Geng <jedhoo@web.de>",
            to=["christian.c.geng@gmail.com"],
            headers={"Reply-To": "jedhoo@gmail.com"})
        # Add template
        # mail.template_id = 'YOUR TEMPLATE ID FROM SENDGRID ADMIN'

        # Replace substitutions in sendgrid template
        mail.substitutions = {'%username%': 'elbuo8'}

        # Attach file
        pdf_file = '/media/win-d/myfiles/2018/mysite_MYSQL/ZSIV/uploads/Bundesgesetzblatt_Teil_II_2021_11.pdf'
        with open(pdf_file, 'rb') as file:
            mail.attachments = [
                (pdf_file, file.read(), 'application/pdf')
            ]

            # Add categories
            mail.categories = [
                'work',
                'urgent',
            ]

            mail.attach_alternative(
                "<p>This is a simple HTML email body</p>", "text/html"
            )

            result = mail.send()
            print(result)
            __import__("pdb").set_trace()


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
