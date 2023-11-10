from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from login.models import User_info  # Import your User_info model
from login.forms import RegisterForm  # Import your RegisterForm

class SignUpViewTest(TestCase):
    def setUp(self):
        self.customer_group, created_customer_group = Group.objects.get_or_create(name='Customer')
        self.queueman_group, created_queueman_group = Group.objects.get_or_create(name='Queueman')
        self.signup_url = reverse('signup')

    def test_signup_valid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'telephone': '1234567890',
            'name': 'Test',
            'surname': 'User',
            'email': 'testuser@example.com',
        }

        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful signup

        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('testpassword123'))  # Check if the password is correctly set

        user_info = User_info.objects.get(username=user)
        self.assertEqual(user_info.telephone, '1234567890')
        self.assertEqual(user_info.name, 'Test')
        self.assertEqual(user_info.surname, 'User')
        self.assertEqual(user_info.email, 'testuser@example.com')

        # Check if the user is in the 'Customer' group
        group = Group.objects.get(name='Customer')
        self.assertTrue(user.groups.filter(name=group.name).exists())
        self.assertRedirects(response, reverse('restaurant_list'))

    def test_signup_invalid_data(self):
        # Test with invalid data, for example, missing required fields
        invalid_data = {}

        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Check if the form is redisplayed with errors

        form_errors = response.context['form'].errors
        self.assertTrue('username' in form_errors)
        self.assertTrue('password1' in form_errors)
        self.assertTrue('telephone' in form_errors)
        # Add more checks for other form fields

    def test_signup_get_request(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)

class LoginViewTest(TestCase):
    def setUp(self):
        # Create test users
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword123')
        self.queueman = User.objects.create_user(username='queueman123', password='testpassword1234')

        # Create groups
        self.customer_group, created_customer_group = Group.objects.get_or_create(name='Customer')
        self.queueman_group, created_queueman_group = Group.objects.get_or_create(name='Queueman')
        # Add users to groups
        if created_customer_group:
            self.customer.groups.add(self.customer_group)
        if created_queueman_group:
            self.queueman.groups.add(self.queueman_group)

        # Set up the login URL
        self.login_url = reverse('login')

    def test_login_successful_redirect_queueman(self):
        response = self.client.post(self.login_url, {'username': 'queueman123', 'password': 'testpassword1234'})
        print(response)
        self.assertEqual(response.url, '/queueman/home/')

        # self.assertRedirects(response,reverse('qhome')) แตก
        self.assertEqual(response.status_code, 302)

    def test_login_successful_redirect_restaurant_list(self):
        # Provide valid credentials for a user not in the Queueman group
        response = self.client.post(self.login_url, {'username': 'testcustomer', 'password': 'testpassword123'})
        print(response)
        self.assertRedirects(response, reverse('restaurant_list'))
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid credentials!')

class LogoutViewTest(TestCase):
    def setUp(self):
        
        self.queueman_group = Group.objects.create(name='Queueman')
        self.customer_group = Group.objects.create(name='Customer')
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword123')
        self.queueman = User.objects.create_user(username='queueman123', password='testpassword1234')
        self.customer.groups.add(self.customer_group)
        self.queueman.groups.add(self.queueman_group)
        self.logout_url = reverse('logout')
        self.client = Client()
        self.client.login(username='testcustomer', password='testpassword123')

    def test_logout_view(self):
        self.client.logout()
        response = self.client.get(reverse('logout'))
        self.assertEqual(200,response.status_code)
        user = authenticate(username='testcustomer', password='testpassword123')
        self.assertIsNotNone(user)  
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Logged out')

