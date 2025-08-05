from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import Contact, CustomUser, Role
from apps.core.models.ownership import City
from apps.core.models.transportation import Car, Driver
from apps.product.models import ProductCategory, Unit


class CoreTransportationViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        self.regular_user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )

        self.unit = Unit.objects.create(name='Test Unit', slug='test-unit')

        self.role = Role.objects.create(role_name='Test Role', role_slug='test-role')
        self.role.units.set([self.unit])

        self.city = City.objects.create(name='Test City', car_code=111)

        self.product_category = ProductCategory.objects.create(name='Test Category', slug='test-category')

        self.contact = Contact.objects.create(name='Test Contact')
        self.contact.units.add(self.unit)

        self.driver = Driver.objects.create(slug='test-driver', contact=self.contact)

        self.car = Car.objects.create(
            city_code=self.city,
            product_category=self.product_category,
            driver=self.driver,
            slug='test-car'
        )

        self.admin_client = APIClient()
        self.user_client = APIClient()
        admin_refresh = RefreshToken.for_user(self.admin_user)
        user_refresh = RefreshToken.for_user(self.regular_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_refresh.access_token}')
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_refresh.access_token}')

    # Driver Tests
    def test_admin_create_driver(self):
        new_contact = Contact.objects.create(name='New Test Contact')
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id, 'slug': 'new-test-driver'}
        response = self.admin_client.post(reverse('admin-driver-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-test-driver')

    def test_admin_create_driver_invalid(self):
        data = {'contact': None, 'slug': ''}
        response = self.admin_client.post(reverse('admin-driver-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_driver(self):
        response = self.admin_client.get(reverse('admin-driver-detail', kwargs={'slug': self.driver.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.driver.slug)

    def test_admin_update_driver(self):
        new_contact = Contact.objects.create(name='New Test Contact')
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id, 'slug': 'updated-driver'}
        response = self.admin_client.put(
            reverse('admin-driver-detail', kwargs={'slug': self.driver.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.slug, 'updated-driver')

    def test_admin_partial_update_driver(self):
        data = {'slug': 'partially-updated-driver'}
        response = self.admin_client.patch(
            reverse('admin-driver-detail', kwargs={'slug': self.driver.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.slug, 'partially-updated-driver')

    def test_admin_delete_driver(self):
        response = self.admin_client.delete(
            reverse('admin-driver-detail', kwargs={'slug': self.driver.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 0)

    def test_admin_list_drivers(self):
        response = self.admin_client.get(reverse('admin-driver-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_create_driver(self):
        new_contact = Contact.objects.create(name='New Test Contact')
        new_contact.units.add(self.unit)
        data = {'contact': new_contact.id, 'slug': 'public-driver'}
        response = self.user_client.post(reverse('driver-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 2)

    def test_public_retrieve_driver(self):
        response = self.user_client.get(reverse('driver-detail', kwargs={'slug': self.driver.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.driver.slug)

    def test_public_list_drivers(self):
        response = self.user_client.get(reverse('driver-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_driver_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('driver-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Car Tests
    def test_admin_create_car(self):
        new_contact = Contact.objects.create(name='New Test Contact 2 ')
        new_contact.units.add(self.unit)
        new_driver = Driver.objects.create(
            slug='new-driver',
            contact=new_contact
        )
        data = {
            'city_code': self.city.id,
            'product_category': self.product_category.id,
            'driver': new_driver.id,
            'slug': 'new-car',
            'alphabet': 'G'
        }
        response = self.admin_client.post(reverse('admin-car-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-car')

    def test_admin_create_car_invalid(self):
        data = {'city_code': None, 'product_category': None, 'driver': None, 'slug': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-car-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_car(self):
        response = self.admin_client.get(reverse('admin-car-detail', kwargs={'slug': self.car.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.car.slug)

    def test_admin_update_car(self):
        new_contact = Contact.objects.create(name='New Test Contact')
        new_contact.units.add(self.unit)
        new_driver = Driver.objects.create(
            slug='new-driver',
            contact=new_contact
        )
        data = {
            'city_code': self.city.id,
            'product_category': self.product_category.id,
            'driver': new_driver.id,
            'slug': 'updated-car',
            'alphabet': 'G'

        }
        response = self.admin_client.put(
            reverse('admin-car-detail', kwargs={'slug': self.car.slug}),
            data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.slug, 'updated-car')

    def test_admin_partial_update_car(self):
        data = {
            'slug': 'partially-updated-car',
            'alphabet': 'G'
        }
        response = self.admin_client.patch(
            reverse('admin-car-detail', kwargs={'slug': self.car.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.slug, 'partially-updated-car')

    def test_admin_delete_car(self):
        response = self.admin_client.delete(
            reverse('admin-car-detail', kwargs={'slug': self.car.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)

    def test_admin_list_cars(self):
        response = self.admin_client.get(reverse('admin-car-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_change_driver_car(self):
        new_contact = Contact.objects.create(name='New Test Contact')
        new_contact.units.add(self.unit)
        new_driver = Driver.objects.create(
            slug='new-driver',
            contact=new_contact
        )
        data = {'driver_id': new_driver.id}
        response = self.admin_client.post(
            reverse('admin-car-change-driver', kwargs={'slug': self.car.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.driver, new_driver)

    def test_admin_change_city_car(self):
        new_city = City.objects.create(name='New City', car_code=111)
        data = {'city_id': new_city.id}
        response = self.admin_client.post(
            reverse('admin-car-change-city', kwargs={'slug': self.car.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.city_code, new_city)

    def test_admin_change_product_category_car(self):
        new_category = ProductCategory.objects.create(name='New Category', slug='new-category')
        data = {'product_category_id': new_category.id}
        response = self.admin_client.post(
            reverse('admin-car-change-product-category', kwargs={'slug': self.car.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.product_category, new_category)

    def test_public_create_car(self):
        new_contact = Contact.objects.create(name='New Test Contact 2 ')
        new_contact.units.add(self.unit)
        new_driver = Driver.objects.create(
            slug='new-driver',
            contact=new_contact
        )
        data = {
            'city_code': self.city.id,
            'product_category': self.product_category.id,
            'driver': new_driver.id,
            'slug': 'public-car',
            'alphabet': 'G'

        }
        response = self.user_client.post(reverse('car-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    def test_public_retrieve_car(self):
        response = self.user_client.get(reverse('car-detail', kwargs={'slug': self.car.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.car.slug)

    def test_public_list_cars(self):
        response = self.user_client.get(reverse('car-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_car_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('car-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)