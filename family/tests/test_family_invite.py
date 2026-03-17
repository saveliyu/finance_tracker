from django.urls import reverse
from .base_view import BaseViewTest
from family.models import *


class InviteViewTest(BaseViewTest):

    def test_invite_creation(self):
        self.client.force_login(self.user)
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:invite'))

        self.assertTrue(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_creation_without_login(self):
        self.client.logout()
        FamilyInvite.objects.all().delete()
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/create_invite/')
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_creation_with_existing_invite(self):
        code = FamilyInvite.objects.create(created_by=self.user, family=self.family).code
        url = reverse('family:create_invite')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('family:invite'))
        self.assertEqual(code, FamilyInvite.objects.filter(created_by=self.user).last().code)

    def test_invite_deletion(self):
        self.client.force_login(self.user)
        FamilyInvite.objects.create(created_by=self.user, family=self.family)
        url = reverse('family:delete_invite')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_empty_invite_deletion(self):
        self.client.force_login(self.user)
        url = reverse('family:delete_invite')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_deletion_without_login(self):
        self.client.logout()
        FamilyInvite.objects.create(created_by=self.user, family=self.family)

        url = reverse('family:delete_invite')
        response = self.client.get(url)

        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/delete_invite/')
        self.assertTrue(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_invite_view(self):
        code = FamilyInvite.objects.create(created_by=self.user, family=self.family).code

        self.client.force_login(self.user)
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, code)

    def test_invite_view_without_login(self):

        self.client.logout()
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertRedirects(response, f'{reverse('users:login', )}?next=/family/invite/')

    def test_empty_invite_view(self):
        FamilyInvite.objects.all().delete()
        self.client.force_login(self.user)
        url = reverse('family:invite')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('family:create_invite'))
        self.assertFalse(FamilyInvite.objects.filter(created_by=self.user).exists())

    def test_enter_invite