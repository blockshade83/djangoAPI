import json
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .model_factories import *

# test api/users/
class AppUserTest(APITestCase):
    # create user instance
    def setUp(self):
        self.user = AppUserFactory.create(first_name='John', last_name='Doe', username='jdoe', email='jdoe@invalid.com')
        self.good_url = reverse('all_users')
        self.bad_url = 'all_users/H'

    def tearDown(self):
        AppUser.objects.all().delete()
        AppUserFactory.reset_sequence(0)

    # test that page is found
    def test_AllUsers_ReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    # test that username is in the API response
    def test_AllUsers_HasRightData(self):
        response = self.client.get(self.good_url, format='json')
        data = json.loads(response.content)
        self.assertTrue(data[0]['username'], self.user.username)

    # test that 404 response is returned when using bad URL
    def test_ReturnFailOnBadURL(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)


# test api/user_posts/<str:username>
class StatusUpdateTest(APITestCase):
    # create user instance and add a status update
    def setUp(self):
        self.user = AppUserFactory.create(first_name='John', last_name='Doe', username='jdoe', email='jdoe@invalid.com')
        self.content = "This is a test message"
        self.status_update = StatusUpdateFactory(author=self.user, content=self.content)
        self.good_url = reverse('get_user_posts', kwargs={'username': self.user.username})

    def tearDown(self):
        AppUser.objects.all().delete()
        StatusUpdate.objects.all().delete()
        AppUserFactory.reset_sequence(0)
        StatusUpdateFactory.reset_sequence(0)

    # test that page is found
    def test_UserPosts_ReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    # test that user's post is found in the API result
    def test_UserPosts_HasRightData(self):
        response = self.client.get(self.good_url, format='json')
        data = json.loads(response.content)
        self.assertEqual(data[0]['email'], self.user.email)
        self.assertEqual(data[0]['content'], self.content)


# test api/user_contacts/<str:username>
class ContactsListTest(APITestCase):
    # create 2 user instances and add one as a contact of the other one
    def setUp(self):
        self.user = AppUserFactory.create(first_name='John', last_name='Doe', username='jdoe', email='jdoe@invalid.com')
        self.contact = AppUserFactory.create(first_name='Mary', last_name='Shelley', username='mshelley', email='mshelley@invalid.com')
        self.user.contacts.add(self.contact)
        self.good_url = reverse('get_user_contacts', kwargs={'username': self.user.username})

    def tearDown(self):
        AppUser.objects.all().delete()
        AppUserFactory.reset_sequence(0)

    # test that page is found
    def test_ContactsList_ReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    # test that user's contact is found in the API result
    def test_ContactsList_HasRightData(self):
        response = self.client.get(self.good_url, format='json')
        data = json.loads(response.content)
        self.assertEquals(data[0]['username'], self.contact.username)


# test api/pending_connection_requests/
class ConnectionRequestTest(APITestCase):
    # create 2 user instances and a connection request from one user to another
    def setUp(self):
        self.user1 = AppUserFactory.create(first_name='John', last_name='Doe', username='jdoe', email='jdoe@invalid.com')
        self.user2 = AppUserFactory.create(first_name='Mary', last_name='Shelley', username='mshelley', email='mshelley@invalid.com')
        self.connection_request = ConnectionRequestFactory(initiated_by=self.user1, sent_to=self.user2)
        self.good_url = reverse('pending_connection_requests')

    def tearDown(self):
        AppUser.objects.all().delete()
        ConnectionRequest.objects.all().delete()
        AppUserFactory.reset_sequence(0)
        ConnectionRequestFactory.reset_sequence(0)

    # test that page is found
    def test_ConnectionRequests_ReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)

    # test that connection request is found in the API result with status pending
    def test_ConnectionRequests_HasRightData(self):
        response = self.client.get(self.good_url, format='json')
        data = json.loads(response.content)
        self.assertEqual(data[0]['from_user']['username'], self.user1.username)
        self.assertEqual(data[0]['to_user']['username'], self.user2.username)
        self.assertEqual(data[0]['status'], 'pending')    