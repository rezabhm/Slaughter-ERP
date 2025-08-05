from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import Contact, CustomUser
from apps.core.models.ownership import City, Agriculture, ProductOwner
from apps.product.models import Product, ProductCategory, Unit


class CoreOwnershipViewsTestCase(TestCase):
    def setUp(self):
        # API clients
        self.client = APIClient()
        self.admin_client = APIClient()
        self.user_client = APIClient()

        # Create users
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass123'
        )
        self.regular_user = CustomUser.objects.create_user(
            username='user', email='user@example.com', password='userpass123'
        )

        # Set JWT authentication credentials
        admin_refresh = RefreshToken.for_user(self.admin_user)
        user_refresh = RefreshToken.for_user(self.regular_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_refresh.access_token}')
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_refresh.access_token}')

        # Create related models
        self.unit = Unit.objects.create(name='Test Unit')
        self.product_category = ProductCategory.objects.create(name='Test Category')

        self.product = Product.objects.create(
            name='Test Product',
            code='TP001',
            category=self.product_category
        )
        self.product.units.add(self.unit)

        self.city = City.objects.create(name='Test City', car_code=11)

        self.contact = Contact.objects.create(name='Test Contact')
        self.contact.units.add(self.unit)

        self.product_owner = ProductOwner.objects.create(contact=self.contact)

        self.agriculture = Agriculture.objects.create(
            name='Test Agriculture',
            city=self.city
        )

    # City Tests
    def test_admin_create_city(self):
        data = {'name': 'New City', 'car_code': 111}
        response = self.admin_client.post(reverse('admin-city-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New City')

    def test_admin_create_city_invalid(self):
        data = {'name': '', 'car_code': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-city-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_city(self):
        response = self.admin_client.get(reverse('admin-city-detail', kwargs={'slug': self.city.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_code'], self.city.car_code)

    def test_admin_update_city(self):
        data = {'name': 'Updated City', 'car_code': 111}
        response = self.admin_client.put(
            reverse('admin-city-detail', kwargs={'slug': self.city.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.city.refresh_from_db()
        self.assertEqual(self.city.name, 'Updated City')

    def test_admin_partial_update_city(self):
        data = {'name': 'Partially Updated City'}
        response = self.admin_client.patch(
            reverse('admin-city-detail', kwargs={'slug': self.city.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.city.refresh_from_db()
        self.assertEqual(self.city.name, 'Partially Updated City')

    def test_admin_delete_city(self):
        response = self.admin_client.delete(
            reverse('admin-city-detail', kwargs={'slug': self.city.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(City.objects.count(), 0)

    def test_admin_list_cities(self):
        response = self.admin_client.get(reverse('admin-city-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_create_city(self):
        data = {'name': 'Public City', 'car_code': 111}
        response = self.user_client.post(reverse('city-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 2)

    def test_public_retrieve_city(self):
        response = self.user_client.get(reverse('city-detail', kwargs={'slug': self.city.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_code'], self.city.car_code)

    def test_public_list_cities(self):
        response = self.user_client.get(reverse('city-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    # Agriculture Tests
    def test_admin_create_agriculture(self):
        data = {'city':self.city.pk, 'name': 'New Agriculture', 'slug': 'new-agriculture'}
        response = self.admin_client.post(reverse('admin-agriculture-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agriculture.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-agriculture')

    def test_admin_create_agriculture_invalid(self):
        data = {'city_id': None, 'product_id': None, 'slug': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-agriculture-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_agriculture(self):
        response = self.admin_client.get(reverse('admin-agriculture-detail', kwargs={'slug': self.agriculture.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.agriculture.slug)

    def test_admin_update_agriculture(self):
        data = {'city_id': self.city.id, 'product_id': self.product.id, 'slug': 'updated-agriculture', 'name':'New Agriculture', 'city':self.city.pk}
        response = self.admin_client.put(
            reverse('admin-agriculture-detail', kwargs={'slug': self.agriculture.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agriculture.refresh_from_db()
        self.assertEqual(self.agriculture.slug, 'test-agriculture')

    def test_admin_partial_update_agriculture(self):
        data = {'slug': 'partially-updated-agriculture'}
        response = self.admin_client.patch(
            reverse('admin-agriculture-detail', kwargs={'slug': self.agriculture.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agriculture.refresh_from_db()
        self.assertEqual(self.agriculture.slug, 'test-agriculture')

    def test_admin_delete_agriculture(self):
        response = self.admin_client.delete(
            reverse('admin-agriculture-detail', kwargs={'slug': self.agriculture.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Agriculture.objects.count(), 0)

    def test_admin_list_agriculture(self):
        response = self.admin_client.get(reverse('admin-agriculture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_change_city_agriculture(self):
        new_city = City.objects.create(name='New City', car_code=111)
        data = {'city_id': new_city.id}
        response = self.admin_client.post(
            reverse('admin-agriculture-change-city', kwargs={'slug': self.agriculture.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agriculture.refresh_from_db()
        self.assertEqual(self.agriculture.city, new_city)

    def test_admin_change_product_agriculture(self):
        new_city = City.objects.create(
            name='New Test City', car_code=11
        )
        data = {'city_id': new_city.id}
        response = self.admin_client.post(
            reverse('admin-agriculture-change-city', kwargs={'slug': self.agriculture.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agriculture.refresh_from_db()
        self.assertEqual(self.agriculture.city, new_city)

    def test_public_create_agriculture(self):
        data = {'city_id': self.city.id, 'product_id': self.product.id, 'slug': 'public-agriculture', 'name':'New Agriculture', 'city':self.city.pk}
        response = self.user_client.post(reverse('agriculture-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agriculture.objects.count(), 2)

    def test_public_retrieve_agriculture(self):
        response = self.user_client.get(reverse('agriculture-detail', kwargs={'slug': self.agriculture.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.agriculture.slug)

    def test_public_list_agriculture(self):
        response = self.user_client.get(reverse('agriculture-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_agriculture_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('agriculture-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Product Owner Tests
    def test_admin_create_product_owner(self):
        data = {'contact': self.contact.id}
        response = self.admin_client.post(reverse('admin-product-owner-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contact']['name'], self.contact.name)

    def test_admin_create_product_owner_invalid(self):
        data = {'contact': None}  # Invalid data
        response = self.admin_client.post(reverse('admin-product-owner-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_product_owner(self):
        response = self.admin_client.get(reverse('admin-product-owner-detail', kwargs={'slug': self.product_owner.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contact']['name'], self.product_owner.contact.name)

    def test_admin_update_product_owner(self):
        new_contact = Contact.objects.create(
            name='New Contact'
        )
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id}
        response = self.admin_client.put(
            reverse('admin-product-owner-detail', kwargs={'slug': self.product_owner.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_owner.refresh_from_db()
        self.assertEqual(self.product_owner.contact, new_contact)

    def test_admin_partial_update_product_owner(self):
        new_contact = Contact.objects.create(
            name='New Contact'
        )
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id}
        response = self.admin_client.patch(
            reverse('admin-product-owner-detail', kwargs={'slug': self.product_owner.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_owner.refresh_from_db()
        self.assertEqual(self.product_owner.contact, new_contact)

    def test_admin_delete_product_owner(self):
        response = self.admin_client.delete(
            reverse('admin-product-owner-detail', kwargs={'slug': self.product_owner.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 1)

    def test_admin_list_product_owners(self):
        response = self.admin_client.get(reverse('admin-product-owner-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_create_product_owner(self):
        new_contact = Contact.objects.create(
            name='New Contact'
        )
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id}
        response = self.user_client.post(reverse('product-owner-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contact']['name'], new_contact.name)

    def test_public_retrieve_product_owner(self):
        response = self.user_client.get(reverse('product-owner-detail', kwargs={'slug': self.product_owner.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contact']['name'], self.product_owner.contact.name)

    def test_public_list_product_owners(self):
        response = self.user_client.get(reverse('product-owner-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_product_owner_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('product-owner-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)