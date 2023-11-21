from django.test import TestCase,Client,RequestFactory
from .models import Restaurant,Historically
from login.models import User_info
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group


class ListRestaurantViewTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='testcustomer', password='testpassword123')
        self.queueman = User.objects.create_user(username='queueman123', password='testpassword1234')

        self.customer_group, created_customer_group = Group.objects.get_or_create(name='Customer')
        self.queueman_group, created_queueman_group = Group.objects.get_or_create(name='Queueman')
        self.restaurant1 = Restaurant.objects.create(name='Restaurant3', location='Location1',phone_number='123',line_id='line99')
        self.restaurant2 = Restaurant.objects.create(name='Restaurant4', location='Location2',phone_number='321',line_id='line88')
        self.restaurant3 = Restaurant.objects.create(name='AnotherRestaurant', location='Location3',phone_number='999',line_id='line100')
        # Add users to groups
        self.customer.groups.add(self.customer_group)
        self.queueman.groups.add(self.queueman_group)
        self.list_restaurant_url = reverse('restaurant_list')
        self.client = Client()
        self.client.login(username='testcustomer', password='testpassword123')
        self.factory = RequestFactory()

    def test_list_restaurant_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,telephone='0985936988',name='kiw',surname='check',email='peerapat@gmail.com')
        Restaurant.objects.create(name='Restaurant1',phone_number='111',location='Location1',line_id='line1')
        Restaurant.objects.create(name='Restaurant2',phone_number='222',location='Location2',line_id='line2')
        response = self.client.get(self.list_restaurant_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_home.html')
        self.assertIn(('Restaurant1','Location1'), response.context['form'])
        self.assertIn(('Restaurant2','Location2'), response.context['form'])
        self.assertEqual(response.context['user'], user_info)
        self.assertEqual(response.context['book_status'], str(user_info.book))
        self.assertEqual(user_info, response.context['user'])

    def test_list_restaurant_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.list_restaurant_url)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)
    
    def test_about_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('about'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_about_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], user_info)
        self.assertEqual(response.context['book_status'], str(user_info.book))

        self.assertTemplateUsed(response, 'customer_about.html')

    def test_wallet_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('wallet'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_wallet_authenticated(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('wallet'))
        self.assertEqual(response.context['user'], user_info)
        self.assertEqual(response.context['book_status'], str(user_info.book))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_wallet.html')

    def test_account_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_account_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                             name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], user_info)
        self.assertEqual(response.context['book_status'], str(user_info.book))
        self.assertTemplateUsed(response, 'customer_account.html')

    def test_edit_page_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('edit_page'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_edit_page_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                             name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('edit_page'))
        self.assertEqual(user_info, response.context['user_profile'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_edit_profile.html')
        self.assertEqual(response.context['user_profile'], user_info)
        self.assertEqual(response.context['book_status'], str(user_info.book))

    def test_success_edit_post_request(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234', \
                                             name='peerapat',surname='ngamsanga',email='example@gmail.com')
        data = {
            'username': 'new_username',
            'name': 'name',
            'surname': 'surname',
            'email': 'example@gmail.com',
            'tele_phone': '123456789',
        }
        response = self.client.post(reverse('success_edit'), data)
        updated_user_info = User_info.objects.get(username=self.customer)

        self.assertEqual(updated_user_info.username.username, 'new_username')
        self.assertEqual(updated_user_info.name, 'name')
        self.assertEqual(updated_user_info.surname, 'surname')
        self.assertEqual(updated_user_info.email, 'example@gmail.com')
        self.assertEqual(updated_user_info.telephone, '123456789')
        self.assertEqual(response.status_code, 200)
    
    def test_success_edit_post_email_exists(self):
        existing_user = User.objects.create_user(username='existinguser', password='testpassword')
        existing_user_info = User_info.objects.create(
            username=existing_user,
            name='Existing',
            surname='User',
            email='existing@example.com',
            telephone='1234567890',
        )
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user_info = User_info.objects.create(
            username=test_user,
            name='test',
            surname='User',
            email='test@example.com',
            telephone='1234567890',
        )
        data = {
            'username': 'testuser',
            'name': 'name',
            'surname': 'surname',
            'email': 'existing@example.com',
            'tele_phone': '123456789',
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('success_edit'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'this email has already been used')

    def test_success_edit_post_username_exists(self):
        existing_user = User.objects.create_user(username='existinguser', password='testpassword')
        existing_user_info = User_info.objects.create(
            username=existing_user,
            name='Existing',
            surname='User',
            email='existing@example.com',
            telephone='1234567890',
        )
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        test_user_info = User_info.objects.create(
            username=test_user,
            name='test',
            surname='User',
            email='test@example.com',
            telephone='1234567890',
        )
        data = {
            'username': 'existinguser',
            'name': 'name',
            'surname': 'surname',
            'email': 'test@example.com',
            'tele_phone': '123456789',
        }
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('success_edit'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'username already use')

    def test_edit_page_authenticated(self):
        test_user = User.objects.create_user(username='testuser', password='testpassword')
        user_info = User_info.objects.create(
            username=test_user,
            name='John',
            surname='Doe',
            email='john@example.com',
            telephone='1234567890',
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_edit_profile.html')
        self.assertTrue('user_profile' in response.context)
        self.assertEqual(response.context['message'], "None")

    def test_edit_page_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('edit_page'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)


    def test_success_edit_witout_post(self):
        user_info = User_info.objects.create(username=self.customer,\
                    telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('success_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_edit_profile.html') 
    
    def test_change_password_unauthenticated_user(self):

        self.client.logout()
        response = self.client.get(reverse('change_password'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)


    def test_change_password_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,\
                    telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_change_password.html')
        self.assertEqual(response.context['book_status'], str(user_info.book))

    def test_success_password_post(self):
        data = {
            'password': 'newpassword123',
        }
        response = self.client.post(reverse('success_password'), data)
        self.assertEqual(response.status_code, 200)
        
    def test_success_password_get(self):
        user_info = User_info.objects.create(username=self.customer,\
                    telephone='1234',name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('success_password'))
        self.assertEqual(response.status_code, 200)
    
    def test_wallet_unauthenticated_user(self):

        self.client.logout()
        response = self.client.get(reverse('history'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)


    def test_history_authenticated_user(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        h1 = Historically.objects.create(username=self.customer.username, \
            restaurant='rest1',cost=200,queeuManName='man1',date='2023-11-07', \
            phone_number_QueueMan='0987654321',phone_number_customer='12345467')
        h2 = Historically.objects.create(username=self.customer.username, \
            restaurant='rest2',cost=300,queeuManName='man2',date='2023-11-07', \
            phone_number_QueueMan='0987654321',phone_number_customer='12345467')
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_history.html')
        self.assertEqual(response.context['book_status'], str(user_info.book))
        self.assertIn(h1,response.context['history'])
        self.assertIn(h2,response.context['history'])

    def test_str_restaurant(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            phone_number='1234567890',
            line_id='test_line_id',
            location='Test Location',
        )

        expected_str = "Test Restaurant 1234567890 test_line_id Test Location"
        self.assertEqual(str(restaurant), expected_str)

    def test_str_historically(self):
        historically_entry = Historically.objects.create(
            username='TestUser',
            restaurant='Test Restaurant',
            cost='100',
            queeuManName='TestQueueMan',
            date='2023-01-01',
            phone_number_QueueMan='1234567890',
            phone_number_customer='9876543210',
        )

        expected_str = "TestUser Test Restaurant 1234567890 9876543210"
        self.assertEqual(str(historically_entry), expected_str)

    def test_verify_gmail_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('verify_gmail'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_search_with_valid_input(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.post(reverse('search'), {'search': 'Restaurant'})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the expected restaurants are present in the response context
        self.assertContains(response, 'Restaurant3')
        self.assertContains(response, 'Location1')
        self.assertContains(response, 'Restaurant4')
        self.assertContains(response, 'Location2')
        self.assertContains(response, 'AnotherRestaurant')
        self.assertContains(response, 'Location3')
        # self.restaurant1 = Restaurant.objects.create(name='Restaurant3', location='Location1',phone_number='123',line_id='line99')
        # self.restaurant2 = Restaurant.objects.create(name='Restaurant4', location='Location2',phone_number='321',line_id='line88')
        # self.restaurant3 = Restaurant.objects.create(name='AnotherRestaurant', location='Location3',phone_number='999',line_id='line100')
    def test_search_with_empty_input(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.post(reverse('search'), {'search': ''})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that all restaurants are present in the response context
        self.assertContains(response, 'Restaurant3')
        self.assertContains(response, 'Location1')
        self.assertContains(response, 'Restaurant4')
        self.assertContains(response, 'Location2')
        self.assertContains(response, 'AnotherRestaurant')
        self.assertContains(response, 'Location3')

    def test_search_with_no_matching_results(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        
        response = self.client.post(reverse('search'), {'search': 'NonExistentRestaurant'})

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the response does not contain any restaurants
        self.assertNotContains(response, 'Restaurant1')
        self.assertNotContains(response, 'Location1')
        self.assertNotContains(response, 'Restaurant2')
        self.assertNotContains(response, 'Location2')
        self.assertNotContains(response, 'AnotherRestaurant')
        self.assertNotContains(response, 'Location3')

    def test_search_redirects_for_non_post_request(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        # Make a GET request to the search view
        response = self.client.get(reverse('search'))
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('restaurant_list'))

    def test_click_rest_post(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        # Define your test data
        data = {'customer': 'numba'}

        # Use reverse to get the URL for your view
        url = reverse('click_rest')

        # Create a POST request
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)