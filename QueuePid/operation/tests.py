from django.test import TestCase,Client,RequestFactory
from customers.models import Restaurant,Historically
from login.models import User_info
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group
from .models import * 
from queueman.models import *
from django.utils import timezone

class TestOpearionApp(TestCase):
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

    def test_booking_view_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('booking'),args=['Test Restaurant'])
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_booking_authenticated(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        response = self.client.get(reverse('booking'))
        self.assertEqual(response.context['book_status'], str(user_info.book))


    def test_customer_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('customer_status'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)


    def test_customer_update_status(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='queueman123', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=True
                                 )
        response = self.client.get(reverse('customer_status'))

        # Refresh the User_info instance from the database
        user_info.refresh_from_db()

        # Check that the 'book' field is set to None
        self.assertIsNone(user_info.book)

        # Check that the Operation instance is deleted
        with self.assertRaises(Operation.DoesNotExist):
            Operation.objects.get(customer_username='testuser')

        # Check that the response redirects to 'restaurant_list'
        self.assertRedirects(response, reverse('restaurant_list'))

    def test_customer_date_not_None(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='queueman123', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False
                                )
        response = self.client.get(reverse('customer_status'))

        # Check that the response has the correct status code
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the expected keys
        self.assertIn('operation', response.context)
        self.assertIn('time_diff', response.context)
        self.assertIn('minute_diff', response.context)
        self.assertIn('hour_diff', response.context)

        # Check that the time differences are calculated as expected
        self.assertEqual(response.context['minute_diff'], 0)
        self.assertEqual(response.context['hour_diff'], 0)

    def test_customer_None_date(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='queueman123', \
                                 date = None,number_Queue=1,number_of_customer=4,update_status=False
                                )
        response = self.client.get(reverse('customer_status'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('operation', response.context)
        self.assertTemplateUsed(response, 'customer_status.html')

    def test_get_number_of_customer_view(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com')
        
        response = self.client.post(reverse('get_number_of_customer'), data={'restaurant_name': 'TestRestaurant', 'number': 5})
        self.assertRedirects(response, reverse('customer_status'))
        self.assertEqual(Booking.objects.count(), 1)
        user_info = User_info.objects.get(username=self.customer)
        self.assertEqual(user_info.book, 'TestRestaurant')
        self.assertEqual(Operation.objects.count(), 1)        
    
    def test_customer_payment_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('customer_payment'))
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(response.status_code, 302)        

    def test_authenticated_payment_post(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp='queueman123'
                                )
        response = self.client.post(reverse('customer_payment'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'customer_review.html')
        user_info.refresh_from_db()
        user_queueman.refresh_from_db()
        self.assertEqual(user_info.credit, 0) 
        self.assertEqual(user_queueman.credit, 30)  
        operation_user.refresh_from_db()
        self.assertEqual(operation_user.cost, '60')

    def test_payment_get(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp='queueman123'
                                )
        response = self.client.get(reverse('customer_payment'))
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the expected keys
        self.assertIn('operation', response.context)
        self.assertIn('price', response.context)
        self.assertIn('credit', response.context)
        self.assertIn('timing_hr', response.context)
        self.assertIn('timing_min', response.context)
        self.assertIn('is_hr', response.context)

        # Add more assertions based on your specific requirements

        # Add assertions based on your template rendering, if necessary
        self.assertTemplateUsed(response, 'customer_payment.html')

    def test_review_get(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp='queueman123'
                                )
        response = self.client.get(reverse('customer_review'))
        self.assertTemplateUsed(response,'customer_review.html')
        self.assertEqual(response.status_code,200)

# not
    def test_post_review(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp='queueman123'
                                )
        response = self.client.post(reverse('customer_review'), data={'rating': 4, 'comment': 'Great service!'})

        # Check that the response redirects to 'restaurant_list'
        self.assertRedirects(response, reverse('restaurant_list'))

        # Check that the Review and Historically instances are created
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Historically.objects.count(), 1)

        # Check that the queueman's star rating is updated
        user_queueman.refresh_from_db()
        self.assertEqual(user_queueman.star, 5.0)

        # Check that the customer's booking status is reset
        user_info.refresh_from_db()
        self.assertIsNone(user_info.book)

        # Check that the Operation instance is deleted
        with self.assertRaises(Operation.DoesNotExist):
            Operation.objects.get(customer_username='testuser')

    def test_non_reivew_post_review(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp='queueman123'
                                )
        response = self.client.post(reverse('customer_review'), data={'comment': 'Great service!'})
        self.assertRedirects(response, reverse('restaurant_list'))
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Historically.objects.count(), 1)
        user_queueman.refresh_from_db()
        self.assertEqual(user_queueman.star, 5.0)
        user_info.refresh_from_db()
        self.assertIsNone(user_info.book)
        with self.assertRaises(Operation.DoesNotExist):
            Operation.objects.get(customer_username='testuser')
        
    def test_cancel_customer(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='queueman123', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp=''
                                )
        response = self.client.get(reverse('customer_cancel'))

        user_info.refresh_from_db()
        user_queueman.refresh_from_db()
        operation_user.refresh_from_db()

        self.assertRedirects(response, reverse('restaurant_list'))
        self.assertEqual(user_info.credit, 0)  # Adjust based on your expected calculation
        self.assertEqual(user_queueman.credit, 30)  # Adjust based on your expected calculation
        self.assertIsNone(user_info.book)
        self.assertTrue(operation_user.update_status)

    def test_book_cancel(self):
        user_info = User_info.objects.create(username=self.customer,telephone='1234',\
                                            name='peerapat',surname='ngamsanga',email='example@gmail.com',credit=60)
        user_queueman = Queueman.objects.create(username=self.queueman,phone_number='1234556',line_id='line000',)
        operation_user = Operation.objects.create(customer_username='testcustomer',restaurant='Restaurant3',cost=0,queueMan_username='queueman123', \
                                 date = timezone.now(),number_Queue=1,number_of_customer=4,update_status=False,temp=''
                                )
        book = Booking.objects.create(customer_username=self.customer,restaurant='Restaurant3',number_of_customer=10)
        response = self.client.get(reverse('cancel_book'))
        self.assertRedirects(response, reverse('restaurant_list'))
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(customer_username=self.customer)
        with self.assertRaises(Operation.DoesNotExist):
            Operation.objects.get(customer_username='testcustomer')


    