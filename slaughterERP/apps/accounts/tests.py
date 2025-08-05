from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import Contact, Role, CustomUser
from apps.product.models import Unit


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass123'
        )
        self.regular_user = CustomUser.objects.create_user(
            username='user', email='user@example.com', password='userpass123'
        )
        self.unit = Unit.objects.create(name='Test Unit', slug='test-unit')
        self.role = Role.objects.create(role_name='Test Role', role_slug='test-role')
        self.role.units.add(self.unit)
        self.contact = Contact.objects.create(name='Test Contact')
        self.admin_user.roles.add(self.role)

        self.admin_client = APIClient()
        self.user_client = APIClient()
        admin_refresh = RefreshToken.for_user(self.admin_user)
        user_refresh = RefreshToken.for_user(self.regular_user)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_refresh.access_token}')
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_refresh.access_token}')

    # User Tests
    def test_admin_create_user(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'roles': [self.role.id]
        }
        response = self.admin_client.post(reverse('admin-users-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertTrue(CustomUser.objects.get(username='newuser').roles.filter(id=self.role.id).exists())

    def test_admin_create_user_invalid(self):
        data = {'username': '', 'email': 'invalid', 'password': 'short'}  # Invalid data
        response = self.admin_client.post(reverse('admin-users-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_user(self):
        response = self.admin_client.get(reverse('admin-users-detail', kwargs={'username': self.regular_user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.regular_user.username)

    def test_admin_update_user(self):
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'roles': [self.role.id],
            'password':'123456:us@'
        }
        response = self.admin_client.put(
            reverse('admin-users-detail', kwargs={'username': self.regular_user.username}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'updateduser')
        self.assertTrue(self.regular_user.roles.filter(id=self.role.id).exists())

    def test_admin_partial_update_user(self):
        data = {'first_name': 'PartiallyUpdated'}
        response = self.admin_client.patch(
            reverse('admin-users-detail', kwargs={'username': self.regular_user.username}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.first_name, 'PartiallyUpdated')

    def test_admin_delete_user(self):
        response = self.admin_client.delete(
            reverse('admin-users-detail', kwargs={'username': self.regular_user.username})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_admin_list_users(self):
        response = self.admin_client.get(reverse('admin-users-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_public_retrieve_user(self):
        response = self.user_client.get(reverse('users-detail', kwargs={'username': self.regular_user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.regular_user.username)

    # Role Tests
    def test_admin_create_role(self):
        data = {'role_name': 'New Role', 'unit_ids': [self.unit.id]}
        response = self.admin_client.post(reverse('admin-role-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)
        self.assertEqual(response.data['role_name'], 'New Role')
        self.assertTrue(Role.objects.get(role_name='New Role').units.filter(id=self.unit.id).exists())

    def test_admin_create_role_invalid(self):
        data = {'role_name': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-role-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_role(self):
        response = self.admin_client.get(reverse('admin-role-detail', kwargs={'role_slug': self.role.role_slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_slug'], self.role.role_slug)

    def test_admin_update_role(self):
        data = {'role_name': 'Updated Role', 'units': [self.unit.id]}
        response = self.admin_client.put(
            reverse('admin-role-detail', kwargs={'role_slug': self.role.role_slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.role_name, 'Updated Role')
        self.assertTrue(self.role.units.filter(id=self.unit.id).exists())

    def test_admin_partial_update_role(self):
        data = {'role_name': 'Partially Updated Role'}
        response = self.admin_client.patch(
            reverse('admin-role-detail', kwargs={'role_slug': self.role.role_slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.role_name, 'Partially Updated Role')

    def test_admin_delete_role(self):
        response = self.admin_client.delete(
            reverse('admin-role-detail', kwargs={'role_slug': self.role.role_slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)

    def test_admin_list_roles(self):
        response = self.admin_client.get(reverse('admin-role-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_role_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('admin-role-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Contact Tests
    def test_admin_create_contact(self):
        data = {'name': 'New Contact', 'unit_ids': [self.unit.id]}
        response = self.admin_client.post(reverse('admin-contact-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Contact')
        self.assertTrue(Contact.objects.get(name='New Contact').units.filter(id=self.unit.id).exists())

    def test_admin_create_contact_invalid(self):
        data = {'name': ''}  # Invalid data
        response = self.admin_client.post(reverse('admin-contact-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_retrieve_contact(self):
        response = self.admin_client.get(reverse('admin-contact-detail', kwargs={'slug': self.contact.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.contact.slug)

    def test_admin_update_contact(self):
        data = {'name': 'Updated Contact', 'unit_ids': [self.unit.id]}
        response = self.admin_client.put(
            reverse('admin-contact-detail', kwargs={'slug': self.contact.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Updated Contact')
        self.assertTrue(self.contact.units.filter(id=self.unit.id).exists())

    def test_admin_partial_update_contact(self):
        data = {'name': 'Partially Updated Contact'}
        response = self.admin_client.patch(
            reverse('admin-contact-detail', kwargs={'slug': self.contact.slug}),
            data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Partially Updated Contact')

    def test_admin_delete_contact(self):
        response = self.admin_client.delete(
            reverse('admin-contact-detail', kwargs={'slug': self.contact.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)

    def test_admin_list_contacts(self):
        response = self.admin_client.get(reverse('admin-contact-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_public_create_contact(self):
        data = {'name': 'Public Contact', 'unit_ids': [self.unit.id]}
        response = self.user_client.post(reverse('contact-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertTrue(Contact.objects.get(name='Public Contact').units.filter(id=self.unit.id).exists())

    def test_public_retrieve_contact(self):
        response = self.user_client.get(reverse('contact-detail', kwargs={'slug': self.contact.slug}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['slug'], self.contact.slug)

    def test_public_list_contacts(self):
        response = self.user_client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_contact_access(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(reverse('contact-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)