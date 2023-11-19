from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User,Group
from .models import Queueman
from login.models import User_info
from operation.models import Operation,Booking
from customers.models import Restaurant

class QhomeViewTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword123')
        self.queueman = User.objects.create_user(username='queueman123', password='testpassword1234')

        self.customer_group, created_customer_group = Group.objects.get_or_create(name='Customer')
        self.queueman_group, created_queueman_group = Group.objects.get_or_create(name='Queueman')
        # self.queueman_info = Queueman.objects.create(username=self.customer ,phone_number='1234',line_id='line')
        # self.customer_info = User_info.objects.create(username=self.customer,telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')

        # Add users to groups
        self.customer.groups.add(self.customer_group)
        self.queueman.groups.add(self.queueman_group)
        self.queueman_info = Queueman.objects.create(username=self.queueman ,phone_number='1234',line_id='line',is_have_queue = False)
        self.customer_info = User_info.objects.create(username=self.customer,telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')
        self.restaurant = Restaurant.objects.create(name = 'test', location = 'eatrh')
        self.booking = Booking.objects.create(customer_username = self.customer, restaurant = self.restaurant.name, number_of_customer = 1)
        self.operation = Operation.objects.create(customer_username = self.customer.username, restaurant = self.restaurant.name, queueMan_username = self.queueman.username, status = 0)
        self.client = Client()
        self.client.login(username='queueman123', password='testpassword1234')

        self.qhome_url = reverse('qhome')

    def test_qhome_view_with_authenticated_user(self):
        response = self.client.get(reverse('qhome'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('clist', response.context)
        self.assertIn('queueman', response.context)
        self.assertEqual(response.context['queueman'].username, self.queueman)  # Adjust this line
        self.assertTemplateUsed(response,'queueman_home.html')

    def test_qhome_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qhome'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_wallet_authenticated_user(self):
        response = self.client.get(reverse('qwallet'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'queueman_wallet.html')
        self.assertEqual(response.context['queueman'],self.queueman_info)

    def test_wallet_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qwallet'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    
    def test_wallet_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qwallet'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_profile_view_with_authenticated_user(self):
        response = self.client.get(reverse('qprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'queueman_profile.html')
        self.assertEqual(response.context['queueman'],self.queueman_info)

    def test_profile_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qprofile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


    def test_edite_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qedit'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_edite_post_authenticated(self):
        data = {
            'username': 'new_usernamecheck',
            'phone_number': 'kiw1231234567',
            'line_id': 'new_line',
        }
        response = self.client.post(reverse('qedit'),data)
        self.assertRedirects(response,reverse('qprofile'))
        self.assertEqual(response.status_code,302)

    def test_edite_no_post_authenticated(self):

        response = self.client.get(reverse('qedit'))
        self.assertTemplateUsed(response,'queueman_edit_profile.html')
        self.assertEqual(response.context['queueman'],self.queueman_info)
        self.assertEqual(response.status_code,200)


    def test_change_password_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qpassword'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    

    def test_edite_view_redirects_for_authenticated_user_post(self):

        data = {
            'password': 'new_password1224',
        }
        response = self.client.post(reverse('qpassword'),data)
        self.assertRedirects(response,reverse('logout'))
        self.assertEqual(response.status_code,302)


    def test_edite_view_redirects_for_authenticated_user_no_post(self):

        response = self.client.get(reverse('qpassword'))
        self.assertTemplateUsed(response,'queueman_change_password.html')
        self.assertEqual(response.status_code,200)

    def test_str_queueman(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')

        queueman_entry = Queueman.objects.create(
            username=user,
            phone_number='1234567890',
            line_id='test_line_id',
            star=5,
            credit=100,
        )

        expected_str = 'testuser'
        self.assertEqual(str(queueman_entry), expected_str)


class StatusTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.queueman = Queueman.objects.create(username=self.user)
        self.customer = User.objects.create_user(username='customer', password='54321')
        self.booking = Booking.objects.create(customer_username=self.customer)
        self.operate = Operation.objects.create(customer_username=self.customer.username, queueMan_username=self.user.username,status = 0)
        self.info = User_info.objects.create(username=self.customer)
        self.client.login(username='testuser', password='12345')


    def test_get_queue(self):
        data = {'customer': self.customer.username}
        response = self.client.post(reverse('qhome'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qstatus'))

        self.assertEqual(Operation.objects.get(pk=self.operate.id).status, 1)
        self.assertEqual(Queueman.objects.get(pk=self.queueman.id).is_have_queue, True)

    def test_status_post_empty_number_queue(self):
        data = {'number_queue': ''}
        response = self.client.post(reverse('qstatus'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qstatus'))

    def test_status_post_update_status_to_in_queue(self):
        self.operate.status = 1
        self.operate.save()

        data = {'number_queue': 10}
        response = self.client.post(reverse('qstatus'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qstatus'))

        self.assertEqual(Operation.objects.get(pk=self.operate.id).status, 2)
        self.assertEqual(Operation.objects.get(pk=self.operate.id).number_Queue, 10)

    def test_status_post_update_number_queue(self):
        self.operate.status = 2
        self.operate.number_Queue = 10
        self.operate.save()

        data = {'number_queue': 5}
        response = self.client.post(reverse('qstatus'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qstatus'))

        self.assertEqual(Operation.objects.get(pk=self.operate.id).number_Queue, 5)

    def test_status_post_finish_queue(self):
        self.operate.status = 2
        self.operate.number_Queue = 0
        self.operate.save()

        response = self.client.post(reverse('qstatus'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qhome'))

        self.assertEqual(Operation.objects.get(pk=self.operate.id).status, 3)
        self.assertEqual(Queueman.objects.get(pk=self.queueman.id).is_have_queue, False)

    def test_cancel(self):
        response = self.client.get(reverse('qcancel'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('qhome'))

        self.assertEqual(Operation.objects.get(pk=self.operate.id).update_status, True)
        self.assertEqual(Queueman.objects.get(pk=self.queueman.id).is_have_queue, False)
