from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class ECommerceTestCase(TestCase):
    def setUp(self):
        # Set up initial data for tests
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_user_registration(self):
        # Test user registration API
        response = self.client.post('/register/', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'profile': {
                'phone': '1234567890',
                'address': '123 Main St'
            },
            'role': 'customer'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User registered successfully')

    def test_user_login(self):
        # Test user login API
        response = self.client.post('/login/', data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    # Add more test cases for user profile, categories, brands, products, cart, checkout, orders, reviews, etc.

class ECommerceAPITestCase(APITestCase):
    def setUp(self):
        # Set up initial data for API tests
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = 'Bearer ' + self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_manage_profile(self):
        # Test manage profile API
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/profile/', data={
            'phone': '9876543210',
            'address': '456 Oak St'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_manage_category(self):
        # Test manage category API
        response = self.client.get('/product-catalog/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post('/product-catalog/categories/', data={
            'name': 'Electronics'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data['id']

        response = self.client.put(f'/product-catalog/categories/{category_id}/', data={
            'name': 'Electronics and Gadgets'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f'/product-catalog/categories/{category_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Add more API test cases for brands, products, cart, checkout, orders, reviews, etc.

