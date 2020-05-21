from django.test import TestCase

# Create your tests here.
from simple_mooc.polls import mail
from django.test.client import Client
from django.urls import reverse

# tem que ter test_algunacoisa
class HomeViewTest(TestCase):

    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('polls:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('polls:home'))
        self.assertTemplateUsed(response,'home.html')
        self.assertTemplateUsed(response,'base.html')
        