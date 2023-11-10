from django.test import TestCase,Client
from .models import Restaurant
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group


class ListRestaurantViewTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword123')
        self.queueman = User.objects.create_user(username='queueman123', password='testpassword1234')

        self.customer_group, created_customer_group = Group.objects.get_or_create(name='Customer')
        self.queueman_group, created_queueman_group = Group.objects.get_or_create(name='Queueman')
        # Add users to groups
        self.list_restaurant_url = reverse('restaurant_list')

    # def test_list_restaurant_authenticated_user(self):
        # Restaurant.objects.create(name='Restaurant1',phone_number='111',location='Location1',line_id='line1')
        # Restaurant.objects.create(name='Restaurant2',phone_number='222',location='Location2',line_id='line2')
        # response = self.client.get(self.list_restaurant_url)
        # self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'customer_home.html')
        # self.assertIn(('Restaurant1', 'Location1'), response.context['form'])
        # self.assertIn(('Restaurant2', 'Location2'), response.context['form'])

    def test_list_restaurant_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.list_restaurant_url)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
        # self.assertContains(response, 'Please log in')

