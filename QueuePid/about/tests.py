from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class AboutViewTest(TestCase):
    def test_more_about_us_view(self):

        response = self.client.get(reverse('more_about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_queuepid_view(self):
        
        response = self.client.get(reverse('queuepid'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'queuepid.html')
    
    def test_about_queuepid_view(self):

        response = self.client.get(reverse('about_queuepid'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_queuepid.html')
