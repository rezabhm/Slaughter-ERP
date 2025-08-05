from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import CustomUser
from apps.product.models import Product, ProductCategory, Unit


class ProductViewsTestCase(TestCase):
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

        self.unit = Unit.objects.create(name='Test Unit')

        self.product_category = ProductCategory.objects.create(name='Test Category')

        self.product = Product.objects.create(
            name='Test Product',
            code='TP001',
            category=self.product_category
        )
        self.product.units.add(self.unit)

        self.admin_client = APIClient()
        self.user_client = APIClient()
        admin_refresh = RefreshToken.for_user(self.admin_user)
        user_refresh = RefreshToken.for_user(self.regular_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_refresh.access_token}')
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_refresh.access_token}')

    # Product Tests
    def test_admin_create_product(self):
        data = {
            'name': 'New Product',
            'code': 'NP001',
            'slug': 'new-product',
            'category': self.product_category.id,
            'units': [self.unit.id]
        }
        response = self.admin_client.post(reverse('admin-product-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-product')

    def test_admin_create_product_invalid(self):
        data = {'name': '', 'code': '', 'slug': '', 'category': None, 'units': None}  # Invalid data
        response = self.admin_client.post(reverse('admin-product-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_product(self):
        response = self.admin_client.get(reverse('admin-product-detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.product.slug)

    def test_admin_update_product(self):
        data = {
            'name': 'Updated Product',
            'code': 'UP001',
            'slug': 'updated-product',
            'category': self.product_category.id,
            'units': [self.unit.id]
        }
        response = self.admin_client.put(
            reverse('admin-product-detail', kwargs={'slug': self.product.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.slug, 'updated-product')

    def test_admin_partial_update_product(self):
        data = {'name': 'Partially Updated Product'}
        response = self.admin_client.patch(
            reverse('admin-product-detail', kwargs={'slug': self.product.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Partially Updated Product')

    def test_admin_delete_product(self):
        response = self.admin_client.delete(
            reverse('admin-product-detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_admin_list_products(self):
        response = self.admin_client.get(reverse('admin-product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_change_category_product(self):
        new_category = ProductCategory.objects.create(name='New Category', slug='new-category')
        data = {'category_id': new_category.id}
        response = self.admin_client.post(
            reverse('admin-product-change-category', kwargs={'slug': self.product.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.category, new_category)

    def test_admin_change_unit_product(self):
        new_unit = Unit.objects.create(name='New Unit', slug='new-unit')
        data = {'unit_id': new_unit.id}
        response = self.admin_client.post(
            reverse('admin-product-change-unit', kwargs={'slug': self.product.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_retrieve_product(self):
        response = self.user_client.get(reverse('product-detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.product.slug)

    def test_public_list_products(self):
        response = self.user_client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_product_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Product Category Tests
    def test_admin_create_product_category(self):
        data = {'name': 'New Category', 'slug': 'new-category'}
        response = self.admin_client.post(reverse('admin-product-category-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductCategory.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-category')

    def test_admin_create_product_category_invalid(self):
        data = {'name': '', 'slug': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-product-category-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_product_category(self):
        response = self.admin_client.get(reverse('admin-product-category-detail', kwargs={'slug': self.product_category.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.product_category.slug)

    def test_admin_update_product_category(self):
        data = {'name': 'Updated Category', 'slug': 'updated-category'}
        response = self.admin_client.put(
            reverse('admin-product-category-detail', kwargs={'slug': self.product_category.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_category.refresh_from_db()
        self.assertEqual(self.product_category.slug, 'updated-category')

    def test_admin_partial_update_product_category(self):
        data = {'name': 'Partially Updated Category'}
        response = self.admin_client.patch(
            reverse('admin-product-category-detail', kwargs={'slug': self.product_category.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_category.refresh_from_db()
        self.assertEqual(self.product_category.name, 'Partially Updated Category')

    def test_admin_delete_product_category(self):
        response = self.admin_client.delete(
            reverse('admin-product-category-detail', kwargs={'slug': self.product_category.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(ProductCategory.objects.count(), 1)

    def test_admin_list_product_categories(self):
        response = self.admin_client.get(reverse('admin-product-category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_retrieve_product_category(self):
        response = self.user_client.get(reverse('product-category-detail', kwargs={'slug': self.product_category.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.product_category.slug)

    def test_public_list_product_categories(self):
        response = self.user_client.get(reverse('product-category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_product_category_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('product-category-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Unit Tests
    def test_admin_create_unit(self):
        data = {'name': 'New Unit', 'slug': 'new-unit'}
        response = self.admin_client.post(reverse('admin-unit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 2)
        self.assertEqual(response.data['slug'], 'new-unit')

    def test_admin_create_unit_invalid(self):
        data = {'name': '', 'slug': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-unit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_unit(self):
        response = self.admin_client.get(reverse('admin-unit-detail', kwargs={'slug': self.unit.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.unit.slug)

    def test_admin_update_unit(self):
        data = {'name': 'Updated Unit', 'slug': 'updated-unit'}
        response = self.admin_client.put(
            reverse('admin-unit-detail', kwargs={'slug': self.unit.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.slug, 'updated-unit')

    def test_admin_partial_update_unit(self):
        data = {'name': 'Partially Updated Unit'}
        response = self.admin_client.patch(
            reverse('admin-unit-detail', kwargs={'slug': self.unit.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.name, 'Partially Updated Unit')

    def test_admin_delete_unit(self):
        response = self.admin_client.delete(
            reverse('admin-unit-detail', kwargs={'slug': self.unit.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Unit.objects.count(), 0)

    def test_admin_list_units(self):
        response = self.admin_client.get(reverse('admin-unit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_create_unit(self):
        data = {'name': 'Public Unit', 'slug': 'public-unit'}
        response = self.user_client.post(reverse('unit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 2)

    def test_public_retrieve_unit(self):
        response = self.user_client.get(reverse('unit-detail', kwargs={'slug': self.unit.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.unit.slug)

    def test_public_list_units(self):
        response = self.user_client.get(reverse('unit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_unit_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('unit-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
