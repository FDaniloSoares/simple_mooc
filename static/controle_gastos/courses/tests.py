from django.test import TestCase

# Create your tests here.
from simple_mooc.polls import mail
from django.test.client import Client
from django.urls import reverse
from simple_mooc.courses.models import Course

# tem que ter test_algunacoisa
class ContactCourseTestCase(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name='Django', slug='django')

    def tearDown(self):
        self.course.delete()

    #@classmethod
    #def setUpClass(cls):
    #pass
    
    #@classmethod
    #def stearDownClass(cls):
    #pass

    def test_contact_form_error(self):
        data = {'name': 'Fulano de Tal', 'email':"", 'message': 'oi'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug]) 
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatorio')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatorio.')