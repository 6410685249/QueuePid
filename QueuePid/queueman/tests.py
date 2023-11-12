from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User,Group
from .models import Queueman
from login.models import User_info
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
        self.queueman_info = Queueman.objects.create(username=self.queueman ,phone_number='1234',line_id='line')
        self.customer_info = User_info.objects.create(username=self.customer,telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')
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

    def test_history_view_with_authenticated_user(self):
        response = self.client.get(reverse('qhistory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'queueman_history.html')
    
    def test_wallet_view_redirects_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('qhistory'))
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